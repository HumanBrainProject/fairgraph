import datetime
import pytest
import fairgraph.openminds.core as omcore
import fairgraph.openminds.publications as ompub
from fairgraph.kgproxy import KGProxy
from fairgraph.caching import object_cache


def test_get_journal():
    jphysiol = ompub.Periodical(name="The Journal of Physiology")
    volume = ompub.PublicationVolume(is_part_of=jphysiol, volume_number="117")
    issue = ompub.PublicationIssue(is_part_of=volume, issue_number="4")
    article = ompub.ScholarlyArticle(
        name="A quantitative description of membrane current and its application to conduction and excitation in nerve",
        authors=[
            omcore.Person(given_name="AL", family_name="Hodgkin"),
            omcore.Person(given_name="AF", family_name="Huxley"),
        ],
        is_part_of=issue,
        publication_date=datetime.date(1952, 8, 1),
        pagination="500–44",
    )
    assert article.get_journal(client=None) == jphysiol
    assert article.get_journal(client=None, with_volume=True) == (jphysiol, volume)
    assert article.get_journal(client=None, with_volume=True, with_issue=True) == (jphysiol, volume, issue)

    expected = "AL Hodgkin & AF Huxley (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. The Journal of Physiology, 117: 500–44."
    assert article.get_citation_string(client=None) == expected


def test_get_journal_with_issue_proxy_journal():
    """When data comes from the KG, volume.is_part_of is a KGProxy, not a resolved Periodical.
    get_journal() should resolve the proxy rather than failing the isinstance assertion."""
    periodical_id = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000001"
    jphysiol = ompub.Periodical(name="The Journal of Physiology", id=periodical_id)
    object_cache[periodical_id] = jphysiol

    try:
        journal_proxy = KGProxy(ompub.Periodical, periodical_id)
        volume = ompub.PublicationVolume(is_part_of=journal_proxy, volume_number="117")
        issue = ompub.PublicationIssue(is_part_of=volume, issue_number="4")
        article = ompub.ScholarlyArticle(
            name="A quantitative description of membrane current and its application to conduction and excitation in nerve",
            authors=[
                omcore.Person(given_name="AL", family_name="Hodgkin"),
                omcore.Person(given_name="AF", family_name="Huxley"),
            ],
            is_part_of=issue,
            publication_date=datetime.date(1952, 8, 1),
            pagination="500–44",
        )
        assert article.get_journal(client=None) == jphysiol
        assert article.get_journal(client=None, with_volume=True) == (jphysiol, volume)
        assert article.get_journal(client=None, with_volume=True, with_issue=True) == (jphysiol, volume, issue)
    finally:
        del object_cache[periodical_id]


def test_get_journal_no_issue():
    jphysiol = ompub.Periodical(name="The Journal of Physiology")
    volume = ompub.PublicationVolume(is_part_of=jphysiol, volume_number="117")
    article = ompub.ScholarlyArticle(
        name="A quantitative description of membrane current and its application to conduction and excitation in nerve",
        authors=[
            omcore.Person(given_name="AL", family_name="Hodgkin"),
            omcore.Person(given_name="AF", family_name="Huxley"),
        ],
        is_part_of=volume,
        publication_date=datetime.date(1952, 8, 1),
        pagination="500–44",
    )
    assert article.get_journal(client=None) == jphysiol
    assert article.get_journal(client=None, with_volume=True) == (jphysiol, volume)
    assert article.get_journal(client=None, with_volume=True, with_issue=True) == (jphysiol, volume, None)

    expected = "AL Hodgkin & AF Huxley (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. The Journal of Physiology, 117: 500–44."
    assert article.get_citation_string(client=None) == expected
