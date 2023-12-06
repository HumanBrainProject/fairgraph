"""
Structured information on an organization.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class Organization(KGObject):
    """
    Structured information on an organization.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/Organization"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the organization."),
        Field("alias", str, "vocab:shortName", doc="Shortened or fully abbreviated name of the organization."),
        Field(
            "affiliations",
            "openminds.core.Affiliation",
            "vocab:affiliation",
            multiple=True,
            doc="Declaration of a person being closely associated to an organization.",
        ),
        Field(
            "digital_identifiers",
            ["openminds.core.GRIDID", "openminds.core.RORID", "openminds.core.RRID"],
            "vocab:digitalIdentifier",
            multiple=True,
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field(
            "has_parents",
            "openminds.core.Organization",
            "vocab:hasParent",
            multiple=True,
            doc="Reference to a parent object or legal person.",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the organization."),
        Field(
            "coordinated_projects",
            "openminds.core.Project",
            "^vocab:coordinator",
            reverse="coordinators",
            multiple=True,
            doc="reverse of 'coordinator'",
        ),
        Field(
            "developed",
            [
                "openminds.computation.ValidationTest",
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipe",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.MetaDataModel",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.Model",
                "openminds.core.ModelVersion",
                "openminds.core.Software",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebService",
                "openminds.core.WebServiceVersion",
            ],
            "^vocab:developer",
            reverse="developers",
            multiple=True,
            doc="reverse of 'developer'",
        ),
        Field(
            "funded",
            "openminds.core.Funding",
            "^vocab:funder",
            reverse="funders",
            multiple=True,
            doc="reverse of 'funder'",
        ),
        Field(
            "has_children",
            "openminds.core.Organization",
            "^vocab:hasParent",
            reverse="has_parents",
            multiple=True,
            doc="reverse of 'hasParent'",
        ),
        Field(
            "has_members",
            "openminds.core.Affiliation",
            "^vocab:memberOf",
            reverse="member_of",
            multiple=True,
            doc="reverse of 'memberOf'",
        ),
        Field(
            "hosts",
            ["openminds.core.FileRepository", "openminds.publications.LivePaperResourceItem"],
            "^vocab:hostedBy",
            reverse="hosted_by",
            multiple=True,
            doc="reverse of 'hostedBy'",
        ),
        Field(
            "is_custodian_of",
            [
                "openminds.core.Dataset",
                "openminds.core.DatasetVersion",
                "openminds.publications.LivePaper",
                "openminds.publications.LivePaperVersion",
                "openminds.sands.BrainAtlas",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpace",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:custodian",
            reverse="custodians",
            multiple=True,
            doc="reverse of 'custodian'",
        ),
        Field(
            "is_owner_of",
            [
                "openminds.ephys.Electrode",
                "openminds.ephys.ElectrodeArray",
                "openminds.ephys.Pipette",
                "openminds.specimenprep.SlicingDevice",
            ],
            "^vocab:owner",
            reverse="owners",
            multiple=True,
            doc="reverse of 'owner'",
        ),
        Field(
            "is_provider_of",
            "openminds.chemicals.ProductSource",
            "^vocab:provider",
            reverse="providers",
            multiple=True,
            doc="reverse of 'provider'",
        ),
        Field(
            "manufactured",
            "openminds.core.Setup",
            "^vocab:manufacturer",
            reverse="manufacturers",
            multiple=True,
            doc="reverse of 'manufacturer'",
        ),
        Field(
            "published",
            [
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.LearningResource",
                "openminds.publications.ScholarlyArticle",
            ],
            "^vocab:publisher",
            reverse="publishers",
            multiple=True,
            doc="reverse of 'publisher'",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        alias=None,
        affiliations=None,
        digital_identifiers=None,
        has_parents=None,
        homepage=None,
        coordinated_projects=None,
        developed=None,
        funded=None,
        has_children=None,
        has_members=None,
        hosts=None,
        is_custodian_of=None,
        is_owner_of=None,
        is_provider_of=None,
        manufactured=None,
        published=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            alias=alias,
            affiliations=affiliations,
            digital_identifiers=digital_identifiers,
            has_parents=has_parents,
            homepage=homepage,
            coordinated_projects=coordinated_projects,
            developed=developed,
            funded=funded,
            has_children=has_children,
            has_members=has_members,
            hosts=hosts,
            is_custodian_of=is_custodian_of,
            is_owner_of=is_owner_of,
            is_provider_of=is_provider_of,
            manufactured=manufactured,
            published=published,
        )
