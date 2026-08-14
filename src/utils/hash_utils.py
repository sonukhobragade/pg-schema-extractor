"""
hash_utils.py -- stable fingerprints for schema object definitions.

Change detection works by comparing a hash of an object's definition against
the hash recorded in the last baseline. That only works if the hash is stable
across things that are not real changes.

Postgres does not hand back a definition byte-for-byte identical every time:
whitespace and line endings vary with server version and how the definition was
originally written. Hashing the raw string means a server upgrade reports every
function in the database as modified, and a change report that cries wolf is a
change report nobody reads.

So the definition is normalised before hashing. Normalisation is deliberately
conservative: it collapses whitespace and strips trailing space, and does
nothing else. It does not lowercase (identifiers can be case-sensitive when
quoted) and it does not strip comments, because a changed comment on a column
is a real change worth surfacing.
"""

import hashlib
import re

# Algorithms permitted by config.yaml's `processing.hash_algorithm`.
_ALGORITHMS = {
    "sha256": hashlib.sha256,
    "sha1": hashlib.sha1,
    "md5": hashlib.md5,
}

_WHITESPACE_RUN = re.compile(r"[ \t\r\f\v]+")
_BLANK_LINES = re.compile(r"\n{2,}")


def normalize_definition(definition: str) -> str:
    """
    Collapse insignificant whitespace in a schema object definition.

    Runs of spaces and tabs become a single space, trailing whitespace on each
    line is dropped, repeated blank lines collapse to one, and the result is
    stripped. Line structure is otherwise preserved so diffs stay readable.
    """
    if not definition:
        return ""

    text = definition.replace("\r\n", "\n").replace("\r", "\n")
    text = _WHITESPACE_RUN.sub(" ", text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = _BLANK_LINES.sub("\n\n", text)
    return text.strip()


def generate_hash(
    definition: str,
    algorithm: str = "sha256",
    normalize: bool = True,
) -> str:
    """
    Return a hex digest fingerprinting a schema object definition.

    Args:
        definition: The object definition as returned by Postgres.
        algorithm: One of sha256, sha1, md5. Defaults to sha256, matching
            `processing.hash_algorithm` in config.yaml.
        normalize: Collapse insignificant whitespace first. Set False only if
            you genuinely want formatting changes reported as changes.

    Raises:
        ValueError: If the algorithm is not recognised. Failing loudly beats
            silently falling back, because a silent change of algorithm
            invalidates every stored baseline at once.
    """
    try:
        hasher = _ALGORITHMS[algorithm]
    except KeyError:
        raise ValueError(
            f"Unsupported hash algorithm {algorithm!r}. "
            f"Expected one of: {', '.join(sorted(_ALGORITHMS))}."
        ) from None

    text = normalize_definition(definition) if normalize else (definition or "")
    return hasher(text.encode("utf-8")).hexdigest()
