"""
Tests for `fairgraph.utility.name_matching`.

Most of this covers fairgraph's own code and is unaffected by where the name-matching helpers come from.

Four classes are tied to the temporary copy of the openMINDS helpers that `name_matching` carries, and
should be deleted/renamed as follows when that copy is replaced by an import:

- `TestRemoveAccents`, `TestMatchesName` and `TestNormalizeName` test the copied helpers
  themselves, and become openMINDS' business rather than ours; delete them.
- `TestParityWithOpenMINDS` is the guard against the copy drifting from the original.
  Once there is nothing to drift, it is still valuable as a check that the delegation is
  wired up and every argument forwarded, but should be renamed accordingly.
"""

# Copyright 2018-2026 CNRS and fairgraph authors and/or their employers

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import pytest

import openminds.v4.controlled_terms
import openminds.v4.sands
import fairgraph.openminds.v4.controlled_terms as omterms
import fairgraph.openminds.v4.sands as omsands
from fairgraph.queries import Regex
from fairgraph.utility.name_matching import (
    MAX_WITHIN_LENGTH,
    build_name_regex,
    build_given_name_regex,
    build_normalized_regex,
    given_names_compatible,
    matches_name,
    names_equivalent,
    narrow_by_name,
    normalize_name,
    remove_accents,
    split_given_names,
)


def kg_search(pattern, value):
    """Match as the KG does: an unanchored, case-insensitive regular expression search."""
    return re.search(pattern, value, re.IGNORECASE) is not None


class TestRemoveAccents:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("Müller", "Muller"),
            ("raphé", "raphe"),
            ("Lorente de Nó", "Lorente de No"),
            ("Straße", "Strasse"),
            ("Œuvre", "OEuvre"),
            ("Ångström", "Angstrom"),
            ("plain", "plain"),
        ],
    )
    def test_remove_accents(self, text, expected):
        assert remove_accents(text) == expected


class TestMatchesName:
    def test_equals_is_case_sensitive_by_default(self):
        assert matches_name("Mus musculus", "Mus musculus")
        assert not matches_name("Mus musculus", "mus musculus")
        assert matches_name("Mus musculus", "mus musculus", case_sensitive=False)

    def test_accents(self):
        assert not matches_name("raphé nuclei", "raphe nuclei")
        assert matches_name("raphé nuclei", "raphe nuclei", ignore_accents=True)
        assert matches_name("raphe nuclei", "raphé nuclei", ignore_accents=True)

    def test_contains_and_within(self):
        assert matches_name("nucleus raphé magnus", "raphé", match="contains")
        assert not matches_name("raphé", "nucleus raphé magnus", match="contains")
        assert matches_name("raphé", "nucleus raphé magnus", match="within")
        assert not matches_name("nucleus raphé magnus", "raphé", match="within")

    def test_invalid_match(self):
        with pytest.raises(ValueError):
            matches_name("a", "a", match="approximately")


class TestBuildNameRegex:
    def test_equals_is_anchored(self):
        pattern = build_name_regex("Mus musculus")
        assert kg_search(pattern, "Mus musculus")
        assert not kg_search(pattern, "Mus musculus domesticus")

    def test_contains_is_not_anchored(self):
        pattern = build_name_regex("musculus", match="contains")
        assert kg_search(pattern, "Mus musculus")
        assert not kg_search(pattern, "Rattus norvegicus")

    def test_special_characters_are_escaped(self):
        pattern = build_name_regex("CC-BY-NC-4.0")
        assert kg_search(pattern, "CC-BY-NC-4.0")
        assert not kg_search(pattern, "CC-BY-NC-4X0")  # the "." must not match any character

    def test_accent_classes(self):
        plain = build_name_regex("raphe nuclei")
        assert kg_search(plain, "raphe nuclei")
        assert not kg_search(plain, "raphé nuclei")
        folding = build_name_regex("raphe nuclei", ignore_accents=True)
        assert kg_search(folding, "raphe nuclei")
        assert kg_search(folding, "raphé nuclei")

    def test_accented_search_string_finds_plain_value(self):
        pattern = build_name_regex("Müller", ignore_accents=True)
        assert kg_search(pattern, "Müller")
        assert kg_search(pattern, "Muller")

    @pytest.mark.parametrize("options", [{"ignore_accents": True}, {"case_sensitive": False}])
    def test_special_letters_expand_both_ways(self, options):
        # casefold() maps "ß" onto "ss", so a case-insensitive search needs this too
        assert kg_search(build_name_regex("Weiss", **options), "Weiß")
        assert kg_search(build_name_regex("Weiß", **options), "Weiss")

    def test_special_letters_are_literal_by_default(self):
        assert not kg_search(build_name_regex("Weiss"), "Weiß")

    def test_within(self):
        pattern = build_name_regex("recordings of Mus musculus", match="within")
        assert kg_search(pattern, "Mus musculus")
        assert kg_search(pattern, "recordings of Mus musculus")
        assert not kg_search(pattern, "Rattus norvegicus")
        assert not kg_search(pattern, "recordings of Mus musculus and more")

    def test_within_with_accents(self):
        pattern = build_name_regex("the raphe nuclei of the rat", match="within", ignore_accents=True)
        assert kg_search(pattern, "raphé nuclei")

    def test_within_length_limit(self):
        with pytest.raises(ValueError):
            build_name_regex("x" * (MAX_WITHIN_LENGTH + 1), match="within")

    def test_invalid_match(self):
        with pytest.raises(ValueError):
            build_name_regex("a", match="approximately")


class TestRegexIsASuperset:
    """
    The regular expression is only a pre-filter; `matches_name()` decides. What must hold is
    that the pre-filter never discards something `matches_name()` would have accepted.
    """

    SEARCHES = ["raphe nuclei", "raphé nuclei", "Müller", "Weiss", "Weiß", "CC-BY-NC-4.0", "Mus musculus"]
    VALUES = [
        "raphe nuclei",
        "raphé nuclei",
        "nucleus raphé magnus",
        "Müller",
        "Muller",
        "müller",
        "Weiss",
        "Weiß",
        "CC-BY-NC-4.0",
        "Mus musculus",
        "mus musculus",
    ]

    @pytest.mark.parametrize("match", ["equals", "contains", "within"])
    @pytest.mark.parametrize("case_sensitive", [True, False])
    @pytest.mark.parametrize("ignore_accents", [True, False])
    def test_superset(self, match, case_sensitive, ignore_accents):
        for search in self.SEARCHES:
            pattern = build_name_regex(
                search, match=match, case_sensitive=case_sensitive, ignore_accents=ignore_accents
            )
            for value in self.VALUES:
                if matches_name(value, search, match, case_sensitive, ignore_accents):
                    assert kg_search(pattern, value), (
                        f"{value!r} matches {search!r} ({match}, case_sensitive={case_sensitive}, "
                        f"ignore_accents={ignore_accents}) but the pre-filter would discard it"
                    )


class TestParityWithOpenMINDS:
    """
    fairgraph's no-client `by_name()` should behave exactly as openMINDS's does.

    These pairs of classes are the same schema: the fairgraph one is used through
    `fairgraph.openminds`, the openMINDS one is the parent it delegates to.
    """

    CASES = [
        (omterms.Species, openminds.v4.controlled_terms.Species, "Mus musculus"),
        (omterms.Species, openminds.v4.controlled_terms.Species, "mus musculus"),
        (omterms.Species, openminds.v4.controlled_terms.Species, "house mouse"),
        (omterms.Species, openminds.v4.controlled_terms.Species, "definitely not a species"),
        (omsands.ParcellationEntity, openminds.v4.sands.ParcellationEntity, "raphé nuclei"),
        (omsands.ParcellationEntity, openminds.v4.sands.ParcellationEntity, "raphe nuclei"),
        (omsands.ParcellationEntity, openminds.v4.sands.ParcellationEntity, "RAPHE NUCLEI"),
        (omsands.ParcellationEntity, openminds.v4.sands.ParcellationEntity, "nucleus"),
    ]

    @pytest.mark.parametrize("fairgraph_cls,openminds_cls,name", CASES)
    @pytest.mark.parametrize("match", ["equals", "contains", "within"])
    @pytest.mark.parametrize("case_sensitive", [True, False])
    @pytest.mark.parametrize("ignore_accents", [True, False])
    def test_parity(self, fairgraph_cls, openminds_cls, name, match, case_sensitive, ignore_accents):
        options = dict(match=match, all=True, case_sensitive=case_sensitive, ignore_accents=ignore_accents)
        ours = fairgraph_cls.by_name(name, **options)
        theirs = openminds_cls.by_name(name, **options)
        assert (ours is None) == (theirs is None)
        if ours is not None:
            assert sorted(obj.id for obj in ours) == sorted(obj.id for obj in theirs)


class TestNormalizeName:
    def test_case_folding_and_accents_are_independent(self):
        assert normalize_name("Raphé") == "Raphé"
        assert normalize_name("Raphé", case_sensitive=False) == "raphé"
        assert normalize_name("Raphé", ignore_accents=True) == "Raphe"
        assert normalize_name("Raphé", case_sensitive=False, ignore_accents=True) == "raphe"


@pytest.mark.parametrize("match", ["equals", "contains", "within"])
@pytest.mark.parametrize("case_sensitive", [True, False])
@pytest.mark.parametrize("ignore_accents", [True, False])
@pytest.mark.parametrize(
    "name", ["CC-BY-NC-4.0", "field CA1, Ammon’s horn [Lorente de Nó]", "a (b) c", "*", "[", "\\", "Weiß"]
)
def test_generated_patterns_are_always_valid(name, match, case_sensitive, ignore_accents):
    # Regex() rejects a malformed pattern, so this also checks that nothing fairgraph
    # generates from a search string containing regex metacharacters is malformed
    pattern = build_name_regex(name, match=match, case_sensitive=case_sensitive, ignore_accents=ignore_accents)
    assert Regex(pattern) == pattern
    # whatever the match type, the search string matches itself
    assert kg_search(pattern, name)


class TestNamesEquivalent:
    @pytest.mark.parametrize(
        "stored,local",
        [
            ("Émilie", "Emilie"),
            ("du Châtelet", "DU CHATELET"),
            ("Ramón y Cajal", "Ramon  y Cajal"),
            (" Lorente de Nó ", "Lorente de No"),
            ("Straße", "Strasse"),
        ],
    )
    def test_equivalent(self, stored, local):
        assert names_equivalent(stored, local)

    @pytest.mark.parametrize(
        "stored,local",
        [
            ("du Châtelet-Lomont", "du Chatelet"),
            ("Ramón y Cajal", "RamonyCajal"),
            ("Emilie", "Emily"),
        ],
    )
    def test_not_equivalent(self, stored, local):
        assert not names_equivalent(stored, local)


class TestBuildNormalizedRegex:
    @pytest.mark.parametrize(
        "stored,local",
        [
            ("Émilie", "Emilie"),
            ("du Châtelet", "DU CHATELET"),
            ("Ramón  y\tCajal ", "Ramon y Cajal"),
            ("Straße", "Strasse"),
            ("Strasse", "Straße"),
            ("Œuvre", "oeuvre"),
            ("Dr. Jekyll (Henry)", "Dr. Jekyll (Henry)"),
        ],
    )
    def test_selects_every_equivalent_value(self, stored, local):
        assert names_equivalent(stored, local)
        assert kg_search(build_normalized_regex(local), stored)

    @pytest.mark.parametrize(
        "stored,local",
        [
            ("du Châtelet-Lomont", "du Chatelet"),
            ("Madame du Châtelet", "du Chatelet"),
            ("Dr X Jekyll", "Dr. Jekyll"),
        ],
    )
    def test_does_not_select_longer_or_different_values(self, stored, local):
        assert not kg_search(build_normalized_regex(local), stored)

    def test_is_a_valid_regex_filter(self):
        Regex(build_normalized_regex("Dr. Jekyll (Henry) [*]"))


class TestNarrowByName:
    class Named:
        def __init__(self, name=None, synonyms=None):
            self.name = name
            self.synonyms = synonyms

    def test_matches_any_property_or_list_item(self):
        a = self.Named(name="raphé nuclei")
        b = self.Named(name="other", synonyms=["raphe nuclei", "x"])
        c = self.Named(name="nucleus raphé magnus")
        assert narrow_by_name([a, b, c], "raphe nuclei", ["name", "synonyms"], ignore_accents=True) == [a, b]
        assert narrow_by_name([a, b, c], "raphé", ["name"], match="contains") == [a, c]


class TestSplitGivenNames:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("James", ["james"]),
            ("James Clerk", ["james", "clerk"]),
            ("  James   C. ", ["james", "c"]),
            ("J.C.", ["j", "c"]),
            ("J. C.", ["j", "c"]),
            ("J C", ["j", "c"]),
            ("Jean-Pierre", ["jean", "pierre"]),
            ("J.-P.", ["j", "p"]),
            ("Émilie", ["emilie"]),
            ("", []),
            (" . ", []),
        ],
    )
    def test_split(self, text, expected):
        assert split_given_names(text) == expected


class TestGivenNamesCompatible:
    @pytest.mark.parametrize(
        "stored,local,expected",
        [
            ("James", "James", True),
            ("James", "James C.", True),
            ("James C.", "James", True),
            ("James C.", "James C", True),
            ("J C", "J.C.", True),
            ("James Clerk", "J. Clerk", True),
            ("J. C.", "J. Clerk", True),
            ("James Clerk", "J.C.", True),
            ("James Clerk", "James", True),
            ("Augusta", "A. Ada", True),
            ("Augusta Ada", "Ada", False),
            ("Clerk", "J. Clerk", False),
            ("James K.", "James C.", False),
            ("Jane", "John", False),
            ("J.-P.", "Jean-Pierre", True),
            ("Émilie", "emilie", True),
            ("James Clerk", "Clerk James", False),
            ("", "James", False),
        ],
    )
    def test_compatible(self, stored, local, expected):
        assert given_names_compatible(stored, local) is expected
        assert given_names_compatible(local, stored) is expected

    def test_an_initial_can_match_any_of_several_names(self):
        # a greedy match of "C." against "Charles" would leave nothing for "Clerk"
        assert given_names_compatible("James Charles Clerk", "James C. Clerk")


class TestBuildGivenNameRegex:
    @pytest.mark.parametrize(
        "local,stored,expected",
        [
            ("James", "James Clerk", True),
            ("J.", "james", True),
            ("James", "  J. C.", True),
            ("Emilie", "Émilie", True),
            ("Émilie", "Emilie", True),
            ("Émilie", "ÉMILIE", True),
            ("Aethel", "Æthel", True),
            ("James", "Clerk James", False),
            ("Emilie", "Amelie", False),
        ],
    )
    def test_matches_names_with_the_same_initial(self, local, stored, expected):
        assert kg_search(build_given_name_regex(local), stored) is expected

    def test_requires_a_given_name(self):
        with pytest.raises(ValueError):
            build_given_name_regex(" ")
