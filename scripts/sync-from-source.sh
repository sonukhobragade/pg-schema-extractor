#!/usr/bin/env bash
# sync-from-source.sh — pull rule/hook improvements forward from the reference
# repo this template was distilled from, instead of hand-diffing.
#
#   bash scripts/sync-from-source.sh --check          # report drift only
#   bash scripts/sync-from-source.sh --apply          # overwrite tier-1/2 files
#   bash scripts/sync-from-source.sh --check --source /path/to/repo
#
# Source resolution order: --source > $TEMPLATE_SOURCE_REPO >
# template.manifest.yaml `upstream.source_repo`.
#
# Files under `upstream.manual_review` are REPORTED but never overwritten —
# they carry project-specific content that a blind copy would destroy.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
REPO_REAL="$(pwd -P)"   # symlink-resolved root, used to contain --apply writes

MODE="check"
SOURCE="${TEMPLATE_SOURCE_REPO:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --check)  MODE="check"; shift ;;
    --apply)  MODE="apply"; shift ;;
    --source) SOURCE="$2"; shift 2 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

MAP_OUT="$(python3 - "$SOURCE" <<'PY'
import re, sys, pathlib

src_override = sys.argv[1]
text = pathlib.Path("template.manifest.yaml").read_text()

# Minimal YAML slice — avoids a PyYAML dependency for a fixed-shape file.
def block(name):
    m = re.search(rf"^  {name}:\n((?:    .*\n|\n)*)", text, re.M)
    return m.group(1) if m else ""

src = src_override
if not src:
    m = re.search(r"^  source_repo:\s*[\"']?([^\"'\n]*)", text, re.M)
    src = (m.group(1).strip() if m else "")

mapping = []
for line in block("mapping").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if ":" in line:
        dst, s = line.split(":", 1)
        mapping.append((dst.strip(), s.strip()))

def listblock(name):
    out = []
    for line in block(name).splitlines():
        line = line.strip()
        if line.startswith("- "):
            out.append(line[2:].split("#", 1)[0].strip())
    return out

allowed = listblock("overwrite_allowed")
manual = listblock("manual_review")

print("SRC=" + src)
for d, s in mapping:
    print(f"MAP\t{d}\t{s}")
for a in allowed:
    print(f"ALLOW\t{a}")
for m in manual:
    print(f"MANUAL\t{m}")
PY
)"

SOURCE="$(printf '%s' "$MAP_OUT" | sed -n 's/^SRC=//p' | head -n 1)"

# A newline inside --source would be serialized into the same newline/tab
# protocol carrying the ALLOW records, letting a crafted value inject an extra
# ALLOW line and get a non-safelisted path overwritten. Reject outright.
case "$SOURCE" in
  *[$'\n\t']*) echo "Source path may not contain newlines or tabs." >&2; exit 2 ;;
esac

if [ -z "$SOURCE" ]; then
  echo "No source repo configured. Set upstream.source_repo in template.manifest.yaml," >&2
  echo "or pass --source /path/to/repo, or export TEMPLATE_SOURCE_REPO." >&2
  exit 2
fi
if [ ! -d "$SOURCE" ]; then
  echo "Source repo not found: $SOURCE" >&2
  exit 2
fi

ALLOWED="$(printf '%s\n' "$MAP_OUT" | sed -n 's/^ALLOW\t//p')"

# The safelist is a LEXICAL check, but `cp` follows symlinks — both on the
# destination itself and on any parent directory. A safelisted path that is (or
# sits under) a symlink would let --apply write a target that is NOT on the
# safelist, possibly outside the repo. So: allowed name AND a real path that
# still resolves inside this repo.
is_allowed() {
  local dst="$1"
  printf '%s\n' "$ALLOWED" | grep -Fxq "$dst" || return 1
  if [ -L "$dst" ]; then
    echo "     !! refusing: $dst is a symlink" >&2
    return 1
  fi
  local parent resolved
  parent="$(cd "$(dirname "$dst")" 2>/dev/null && pwd -P)" || return 1
  resolved="$parent/$(basename "$dst")"
  case "$resolved" in
    "$REPO_REAL"/*) return 0 ;;
    *) echo "     !! refusing: $dst resolves outside the repo ($resolved)" >&2
       return 1 ;;
  esac
}

# Truncated diff. Buffered into a variable first: piping `diff` into `head`
# gives diff a SIGPIPE, which under `set -e` aborts the whole run after the
# first drifted file.
show_diff() {
  local out
  out="$(diff -u "$1" "$2" 2>/dev/null || true)"
  printf '%s\n' "$out" | sed -n '1,40s/^/     /p'
  if [ "$(printf '%s\n' "$out" | wc -l)" -gt 40 ]; then
    echo "     ... (truncated; run: diff -u $1 $2)"
  fi
}

drift=0
changed=0
skipped=0

echo "== Tracked files (source: $SOURCE) =="
while IFS=$'\t' read -r tag dst src; do
  [ "$tag" = "MAP" ] || continue
  s="$SOURCE/$src"
  if [ ! -f "$s" ]; then
    # A declared mapping we could not check is NOT "no drift" — saying so would
    # report success while a tracked file went unverified.
    echo "  ?? upstream missing (mapping unverified): $src"
    drift=1
    continue
  fi
  if [ ! -f "$dst" ]; then
    echo "  ++ new upstream file -> $dst"
    drift=1
    if [ "$MODE" = "apply" ]; then
      mkdir -p "$(dirname "$dst")"
      if is_allowed "$dst"; then
        cp "$s" "$dst"; changed=$((changed+1))
      fi
    fi
    continue
  fi
  if diff -q "$s" "$dst" >/dev/null 2>&1; then
    echo "  == in sync: $dst"
    continue
  fi

  drift=1
  if is_allowed "$dst"; then
    echo "  ~~ DRIFT (overwrite allowed): $dst  (vs $src)"
    if [ "$MODE" = "apply" ]; then
      cp "$s" "$dst"; changed=$((changed+1))
      echo "     -> overwritten; re-run scripts/init.sh to re-apply placeholders"
    else
      show_diff "$dst" "$s"
    fi
  else
    # Generalized file: upstream's copy is project-specific. Report, never write.
    echo "  ~~ DRIFT (port by hand — NOT overwritten): $dst  (vs $src)"
    skipped=$((skipped+1))
    show_diff "$dst" "$s"
  fi
done < <(printf '%s\n' "$MAP_OUT")

echo
echo "== Project-owned files (no upstream counterpart, never compared) =="
while IFS=$'\t' read -r tag path _; do
  [ "$tag" = "MANUAL" ] || continue
  echo "  -- $path"
done < <(printf '%s\n' "$MAP_OUT")

echo
if [ "$MODE" = "apply" ]; then
  echo "Applied $changed file(s)."
  [ "$skipped" -gt 0 ] && cat <<EOF
$skipped file(s) drifted but were NOT overwritten — they are generalized copies
whose upstream version is project-specific. Read the diffs above, take the idea,
and port it by hand keeping the generalized wording. To opt a file into
auto-overwrite, add it to \`overwrite_allowed\` in template.manifest.yaml.
EOF
  [ "$changed" -gt 0 ] && echo "NOTE: overwritten templated files may contain raw placeholders — re-run: bash scripts/init.sh"
else
  if [ "$drift" -eq 0 ]; then
    echo "No drift."
  else
    echo "Drift found. --apply writes only files in \`overwrite_allowed\`;"
    echo "the rest are reported for hand-porting."
  fi
fi
exit 0
