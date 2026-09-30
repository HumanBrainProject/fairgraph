"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.publications import Book as OMBook
from fairgraph import KGObject


from datetime import date
from openminds import IRI


class Book(KGObject, OMBook):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Book"
    default_space = "livepapers"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_parts",
            "openminds.v5.publications.Chapter",
            "isPartOf",
            reverse="is_part_of",
            multiple=True,
            description="reverse of 'is_part_of'",
        ),
        Property(
            "related_to",
            [
                "openminds.v5.computation.ValidationTest",
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipe",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Dataset",
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.Interface",
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.Service",
                "openminds.v5.core.Software",
                "openminds.v5.core.SoftwareVersion",
                "openminds.v5.publications.LivePaper",
                "openminds.v5.publications.LivePaperVersion",
                "openminds.v5.sands.AnatomicalAtlas",
                "openminds.v5.sands.AnatomicalAtlasVersion",
                "openminds.v5.sands.CommonCoordinateFramework",
                "openminds.v5.sands.CommonCoordinateFrameworkVersion",
            ],
            "relatedPublication",
            reverse="related_publications",
            multiple=True,
            description="reverse of 'related_publications'",
        ),
    ]
    existence_query_properties = ("name", "publication_date")

    def __init__(
        self,
        name=None,
        abstract=None,
        cited_publications=None,
        contributions=None,
        contributor_affiliations=None,
        copyright=None,
        creation_date=None,
        digital_identifier=None,
        funding=None,
        has_parts=None,
        iri=None,
        keywords=None,
        modification_date=None,
        publication_date=None,
        related_to=None,
        usage_conditions=None,
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
            cited_publications=cited_publications,
            contributions=contributions,
            contributor_affiliations=contributor_affiliations,
            copyright=copyright,
            creation_date=creation_date,
            digital_identifier=digital_identifier,
            funding=funding,
            has_parts=has_parts,
            iri=iri,
            keywords=keywords,
            modification_date=modification_date,
            publication_date=publication_date,
            related_to=related_to,
            usage_conditions=usage_conditions,
            version_identifier=version_identifier,
        )
