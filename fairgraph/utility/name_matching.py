"""
Helpers for matching metadata objects by name.

The first block below is a **verbatim copy** of the helpers that openMINDS generates into
every one of its ``by_name()`` methods. They are closures there, repeated in each of the
406 generated modules, so they cannot be imported. openMINDS_Python PR #106 moves them to
``openminds.base``; once fairgraph requires a release containing it, delete the block and
uncomment the import line, and bump ``openminds>=`` in pyproject.toml.

Everything after the block is fairgraph-specific: it *calls* the helpers above rather than
restating anything they know, so the swap changes no behaviour.

While the copy is in place, ``TestParityWithOpenMINDS`` in ``test_name_matching.py``
guards against it drifting from the original.
"""

import re
from unicodedata import combining, normalize as unicode_normalize
from typing import Any, Dict, Iterable, List, Set, Tuple

from .misc import as_list

# --- begin temporary copy of the openMINDS helpers ---------------------------------------
#
# from openminds.base import (
#     MATCH_TYPES, NAMELIKE_PROPERTIES, SPECIAL_LETTERS, matches_name, normalize_name, remove_accents
# )

NAMELIKE_PROPERTIES = ("name", "lookup_label", "family_name", "full_name", "short_name", "abbreviation")

MATCH_TYPES = ("equals", "contains", "within")

SPECIAL_LETTERS = str.maketrans(
    {
        "Ł": "L",
        "ł": "l",
        "Ø": "O",
        "ø": "o",
        "Đ": "D",
        "đ": "d",
        "Ð": "D",
        "ð": "d",
        "Þ": "Th",
        "þ": "th",
        "Æ": "AE",
        "æ": "ae",
        "Œ": "OE",
        "œ": "oe",
        "ß": "ss",
        "ẞ": "SS",
        "Ə": "E",
        "ə": "e",
        "ı": "i",
    }
)


def remove_accents(s: str) -> str:
    """
    Strip accents (acute, grave, circumflex) and other diacritical marks (cedilla, tilde,
    ring, etc.), and replace special letters (ß, œ, æ, ø, ł, etc.) by their closest
    plain-letter equivalents (e.g. "ß" by "ss").
    """
    nfd_form = unicode_normalize("NFD", s)
    stripped = "".join(c for c in nfd_form if not combining(c))
    return stripped.translate(SPECIAL_LETTERS)


def normalize_name(s: str, case_sensitive: bool = True, ignore_accents: bool = False) -> str:
    """Put a name-like string into the form in which names are compared."""
    if not case_sensitive:
        s = s.casefold()
    if ignore_accents:
        s = remove_accents(s)
    return s


def matches_name(
    value: str,
    query: str,
    match: str = "equals",
    case_sensitive: bool = True,
    ignore_accents: bool = False,
) -> bool:
    """
    Whether the name-like value `value` matches the search string `query`.

    Args:
        value (str): a name-like property value belonging to a metadata object.
        query (str): the string being searched for.
        match (str, optional): either "equals" (exact match - default), "contains"
            (`value` contains `query`), or "within" (`query` contains `value`).
        case_sensitive (bool, optional): Whether the comparison should be case-sensitive.
            Defaults to True.
        ignore_accents (bool, optional): Whether to ignore accents and other diacritical
            marks, and treat special letters as their plain-letter equivalents, when
            matching. Defaults to False.
    """
    normalized_value = normalize_name(value, case_sensitive, ignore_accents)
    normalized_query = normalize_name(query, case_sensitive, ignore_accents)
    if match == "equals":
        return normalized_value == normalized_query
    elif match == "contains":
        return normalized_query in normalized_value
    elif match == "within":
        return normalized_value in normalized_query
    else:
        raise ValueError("'match' must be either 'equals', 'contains', or 'within'")


# --- end temporary copy of the openMINDS helpers -----------------------------------------


#: `synonyms` is list-valued, and openMINDS handles it separately from the properties above,
#: but as far as searching the KG is concerned it is just one more place a name can be found.
KG_NAMELIKE_PROPERTIES = NAMELIKE_PROPERTIES + ("synonyms",)

#: The Unicode blocks in which `remove_accents()` can do anything: Latin-1 Supplement,
#: Latin Extended-A and -B, and Latin Extended Additional.
_LATIN_RANGES = ((0x00C0, 0x024F), (0x1E00, 0x1EFF))

#: Longest search string for which a `match="within"` KG query is built. The pattern grows
#: with the square of the length, so beyond this we refuse rather than emit something huge.
MAX_WITHIN_LENGTH = 100

_fold_maps_cache = None


def _fold_maps() -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Return (single, multi): mappings from a plain-letter form to the characters that fold onto it,
    split by whether that form is one character ("u" <- "ù", "ü", ...) or several ("ss" <- "ß", "ae" <- "æ", ...).

    Built by calling `remove_accents()`, so it cannot drift from it.
    """
    global _fold_maps_cache
    if _fold_maps_cache is None:
        single: Dict[str, Set[str]] = {}
        multi: Dict[str, Set[str]] = {}
        for start, end in _LATIN_RANGES:
            for code_point in range(start, end + 1):
                character = chr(code_point)
                folded = remove_accents(character)
                if not folded or folded == character:
                    continue
                target = single if len(folded) == 1 else multi
                target.setdefault(folded, set()).add(character)
        _fold_maps_cache = (single, multi)
    return _fold_maps_cache


def _alternation(alternatives: Set[str]) -> str:
    return "(?:" + "|".join(re.escape(alternative) for alternative in sorted(alternatives)) + ")"


def _expand(text: str, case_sensitive: bool, ignore_accents: bool) -> str:
    """
    Turn a search string into a regular expression matching every spelling of it that
    `matches_name()` would consider equal, under the given options.

    The KG's REGEX filter is always case-insensitive, so case is not expressed here;
    it is enforced by the local `matches_name()` pass instead.
    What must be expressed is the folding of accented and special letters, which the KG does not do.
    """
    single, multi = _fold_maps()
    # casefold() maps "ß" onto "ss", so the special letters need expanding for a
    # case-insensitive search too, not only when accents are being ignored
    expand_special = ignore_accents or not case_sensitive
    parts = []
    index = 0
    while index < len(text):
        character = text[index]
        chunk = None
        if expand_special:
            pair = text[index : index + 2]
            if len(pair) == 2 and pair in multi:
                parts.append(_alternation({pair} | multi[pair]))
                index += 2
                continue
            folded = remove_accents(character)
            if len(folded) > 1:  # a special letter, e.g. "ß" -> "ss"
                chunk = _alternation({character, folded} | multi.get(folded, set()))
        if chunk is None and ignore_accents:
            folded = remove_accents(character)
            variants = {character, folded} | single.get(folded, set())
            if len(variants) > 1:
                chunk = "[" + "".join(re.escape(variant) for variant in sorted(variants)) + "]"
        parts.append(chunk if chunk is not None else re.escape(character))
        index += 1
    return "".join(parts)


def build_name_regex(
    name: str,
    match: str = "equals",
    case_sensitive: bool = True,
    ignore_accents: bool = False,
) -> str:
    """
    Build a regular expression for use as a KG `REGEX` filter on a name-like property.

    The pattern is deliberately permissive: it is a pre-filter which should return a
    superset of the true matches, which `matches_name()` then narrows exactly.
    The KG's REGEX operator is an unanchored, case-insensitive search which does no accent folding,
    so anchors and character classes are added here as required, and everything taken from the
    search string itself is escaped, so that a name containing "." or "(" is looked for literally.

    Args:
        name (str): the string being searched for.
        match (str, optional): "equals", "contains" or "within". See `matches_name()`.
        case_sensitive (bool, optional): Defaults to True.
        ignore_accents (bool, optional): Defaults to False.
    """
    if match == "equals":
        return f"^{_expand(name, case_sensitive, ignore_accents)}$"
    elif match == "contains":
        return _expand(name, case_sensitive, ignore_accents)
    elif match == "within":
        return _build_within_regex(name, case_sensitive, ignore_accents)
    else:
        raise ValueError("'match' must be either 'equals', 'contains', or 'within'")


def _build_within_regex(name: str, case_sensitive: bool, ignore_accents: bool) -> str:
    """
    Build a pattern matching any value that is contained in `name`.

    There is no KG filter for "this property is a substring of the given string", so we
    enumerate the substrings of the search string and match against all of them.
    Folding is applied to the search string first, and undone by `_expand()` when each substring is
    turned into a pattern, so that, for example, a stored "Müller" is still reachable from a search
    for "Muller Institute" with `ignore_accents`.
    """
    if ignore_accents:
        base = remove_accents(name)
    elif not case_sensitive:
        # casefold() folds the special letters but leaves accents alone
        base = name.translate(SPECIAL_LETTERS)
    else:
        base = name
    if len(base) > MAX_WITHIN_LENGTH:
        raise ValueError(
            f"match='within' is limited to search strings of {MAX_WITHIN_LENGTH} characters "
            f"or fewer when querying the KG (got {len(base)})"
        )
    if not base:
        return "^$"
    substrings = {base[i:j] for i in range(len(base)) for j in range(i + 1, len(base) + 1)}
    ordered = sorted(substrings, key=lambda s: (-len(s), s))
    return "^(?:" + "|".join(_expand(substring, case_sensitive, ignore_accents) for substring in ordered) + ")$"


def narrow_by_name(
    objects: Iterable[Any],
    name: str,
    property_names: Iterable[str],
    match: str = "equals",
    case_sensitive: bool = True,
    ignore_accents: bool = False,
) -> List[Any]:
    """
    Return those of `objects` for which a value of one of the properties `property_names` matches `name`.

    This is the local step that follows a KG query pre-filtered with `build_name_regex()`,
    which returns a superset of the true matches.
    """
    property_names = list(property_names)
    return [
        obj
        for obj in objects
        if any(
            matches_name(value, name, match, case_sensitive, ignore_accents)
            for property_name in property_names
            for value in as_list(getattr(obj, property_name, None))
            if isinstance(value, str)
        )
    ]


def collapse_whitespace(value: str) -> str:
    """Remove leading and trailing whitespace, and replace each run of whitespace inside `value` by a single space."""
    return " ".join(value.split())


def build_normalized_regex(value: str) -> str:
    """
    Build a regular expression for use as a KG `REGEX` filter, which selects the stored values that
    `names_equivalent()` considers equivalent to `value` (and possibly a few more, since the KG
    ignores case in a slightly different way to `casefold()`).

    Case and accents are ignored, and so are differences in whitespace: any run of whitespace
    matches any other, and leading and trailing whitespace in the stored value is allowed.
    """
    tokens = value.split()
    body = r"\s+".join(_expand(token, case_sensitive=False, ignore_accents=True) for token in tokens)
    return rf"^\s*{body}\s*$"


def names_equivalent(stored: str, local: str) -> bool:
    """
    Whether two strings are the same name, ignoring case, accents and other diacritical marks,
    special letters (e.g. "ß" and "ss"), and differences in whitespace.
    """
    return matches_name(
        collapse_whitespace(stored), collapse_whitespace(local), "equals", case_sensitive=False, ignore_accents=True
    )


def split_given_names(value: str) -> List[str]:
    """
    Split a string containing one or more given names into its parts, in the form in which they are compared
    by `given_names_compatible()`: without case, accents or full stops.

    Names are separated by whitespace, by hyphens, or by the full stop after an initial,
    so "J.-P." and "Jean-Pierre" both have two parts, and so do "J.E." and "J. E.".
    """
    tokens = re.split(r"[\s\-‐‑–]+|(?<=\.)", value)
    parts = []
    for token in tokens:
        token = remove_accents(token.casefold()).strip(".")
        if token:
            parts.append(token)
    return parts


def _given_name_parts_compatible(a: str, b: str) -> bool:
    """Whether two parts of a given name may be the same name: they are equal, or one is the initial of the other."""
    if a == b:
        return True
    if len(a) == 1:
        return b.startswith(a)
    if len(b) == 1:
        return a.startswith(b)
    return False


def _is_ordered_subset(shorter: List[str], longer: List[str]) -> bool:
    """Whether each of `shorter` corresponds to a different item of `longer`, in the same order."""
    if not shorter:
        return True
    for index, part in enumerate(longer):
        if _given_name_parts_compatible(shorter[0], part) and _is_ordered_subset(shorter[1:], longer[index + 1 :]):
            return True
    return False


def given_names_compatible(stored: str, local: str) -> bool:
    """
    Whether two strings of given names may belong to the same person, allowing for middle names that appear
    in only one of them, and for initials in place of names.

    The first names must correspond: they must be the same (ignoring case, accents and full stops),
    or one must be the initial of the other. Each of the remaining names in the string with fewer of them
    must correspond in the same way to one of the remaining names in the other, in the same order.
    So "James" and "J. Clerk" are both compatible with "James Clerk", but "Clerk" is not,
    and neither is "James K.".
    """
    stored_parts = split_given_names(stored)
    local_parts = split_given_names(local)
    if not (stored_parts and local_parts):
        return False
    if not _given_name_parts_compatible(stored_parts[0], local_parts[0]):
        return False
    shorter, longer = sorted((stored_parts[1:], local_parts[1:]), key=len)
    return _is_ordered_subset(shorter, longer)


def build_given_name_regex(value: str) -> str:
    """
    Build a regular expression for use as a KG `REGEX` filter, which selects the stored given names that
    `given_names_compatible()` might consider compatible with `value`: those starting with the same letter,
    ignoring case and accents. It is a pre-filter, whose results are checked with `given_names_compatible()`.
    """
    parts = split_given_names(value)
    if not parts:
        raise ValueError(f"No given name found in {value!r}")
    single, multi = _fold_maps()
    # both cases are listed, in case the KG ignores case only for unaccented letters
    initials = {parts[0][0], parts[0][0].upper()}
    alternatives = set(initials)
    for initial in initials:
        alternatives |= single.get(initial, set())
    # a stored name may begin with a special letter that folds onto two letters, e.g. "Æ" -> "AE"
    alternatives |= {
        character for folded, characters in multi.items() if folded[0] in initials for character in characters
    }
    return r"^\s*" + "[" + "".join(re.escape(alternative) for alternative in sorted(alternatives)) + "]"
