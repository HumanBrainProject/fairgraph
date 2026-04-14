"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.publications import ScholarlyArticle as OMScholarlyArticle
from fairgraph import KGObject

from fairgraph.utility import as_list
from .publication_issue import PublicationIssue
from .periodical import Periodical
from datetime import date
from openminds import IRI


class ScholarlyArticle(KGObject, OMScholarlyArticle):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ScholarlyArticle"
    default_space = "livepapers"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "related_to",
            [
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebServiceVersion",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "relatedPublication",
            reverse="related_publications",
            multiple=True,
            description="reverse of 'related_publications'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        abstract=None,
        authors=None,
        cited_publications=None,
        copyright=None,
        creation_date=None,
        custodians=None,
        digital_identifier=None,
        editors=None,
        funding=None,
        iri=None,
        is_part_of=None,
        keywords=None,
        license=None,
        modification_date=None,
        pagination=None,
        publication_date=None,
        publisher=None,
        related_to=None,
        version_identifier=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            name=name,
            abstract=abstract,
            authors=authors,
            cited_publications=cited_publications,
            copyright=copyright,
            creation_date=creation_date,
            custodians=custodians,
            digital_identifier=digital_identifier,
            editors=editors,
            funding=funding,
            iri=iri,
            is_part_of=is_part_of,
            keywords=keywords,
            license=license,
            modification_date=modification_date,
            pagination=pagination,
            publication_date=publication_date,
            publisher=publisher,
            related_to=related_to,
            version_identifier=version_identifier,
        )

    def get_journal(self, client, with_volume=False, with_issue=False):
        journal = volume = issue = None
        if self.is_part_of:
            issue_or_volume = self.is_part_of.resolve(
                client, release_status=self.release_status, follow_links={"is_part_of": {}}
            )
            if isinstance(issue_or_volume, PublicationIssue):
                volume = issue_or_volume.is_part_of
                issue = issue_or_volume
            else:
                volume = issue_or_volume
                issue = None
            journal = volume.is_part_of
            if not isinstance(journal, Periodical):
                journal = journal.resolve(client, release_status=self.release_status)
        retval = [journal]
        if with_volume:
            retval.append(volume)
        if with_issue:
            retval.append(issue)
        if not with_volume and not with_issue:
            return journal
        else:
            return tuple(retval)

    def get_citation_string(self, client):
        # Eyal, G., Verhoog, M. B., Testa-Silva, G., Deitcher, Y., Lodder, '
        #     -              'J. C., Benavides-Piccione, R., ... & Segev, I. (2016). Unique '
        #     -              'membrane properties and enhanced signal processing in human '
        #     -              'neocortical neurons. Elife, 5, e16553.
        self.resolve(client, follow_links={"is_part_of": {}, "authors": {}})
        authors = as_list(self.authors)
        if len(authors) == 1:
            author_str = authors[0].full_name
        elif len(authors) > 1:
            author_str = ", ".join(au.full_name for au in authors[:-1])
            author_str += " & " + self.authors[-1].full_name
        journal, volume, issue = self.get_journal(client, with_volume=True, with_issue=True)
        title = self.name
        if title and title[-1] != ".":
            title += "."
        journal_name = journal.name if journal else ""
        volume_number = f"{volume.volume_number}: " if (volume and volume.volume_number != "placeholder") else ""
        year = self.publication_date.year if self.publication_date else "unpublished?"
        return f"{author_str} ({year}). {title} {journal_name}, {volume_number}{self.pagination or ''}."
