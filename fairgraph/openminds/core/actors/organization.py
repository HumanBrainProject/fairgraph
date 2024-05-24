"""
Structured information on an organization.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from fairgraph.base import IRI


class Organization(KGObject):
    """
    Structured information on an organization.
    """

    default_space = "common"
    type_ = "https://openminds.ebrains.eu/core/Organization"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "affiliations",
            "openminds.core.Affiliation",
            "vocab:affiliation",
            multiple=True,
            doc="Declaration of a person being closely associated to an organization.",
        ),
        Property(
            "digital_identifiers",
            ["openminds.core.GRIDID", "openminds.core.RORID", "openminds.core.RRID"],
            "vocab:digitalIdentifier",
            multiple=True,
            doc="Digital handle to identify objects or legal persons.",
        ),
        Property(
            "full_name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the organization."
        ),
        Property(
            "has_parents",
            "openminds.core.Organization",
            "vocab:hasParent",
            multiple=True,
            doc="Reference to a parent object or legal person.",
        ),
        Property("homepage", IRI, "vocab:homepage", doc="Main website of the organization."),
        Property("short_name", str, "vocab:shortName", doc="Shortened or fully abbreviated name of the organization."),
    ]
    reverse_properties = [
        Property(
            "coordinated_projects",
            "openminds.core.Project",
            "^vocab:coordinator",
            reverse="coordinators",
            multiple=True,
            doc="reverse of 'coordinator'",
        ),
        Property(
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
        Property(
            "funded",
            "openminds.core.Funding",
            "^vocab:funder",
            reverse="funders",
            multiple=True,
            doc="reverse of 'funder'",
        ),
        Property(
            "has_children",
            "openminds.core.Organization",
            "^vocab:hasParent",
            reverse="has_parents",
            multiple=True,
            doc="reverse of 'hasParent'",
        ),
        Property(
            "has_members",
            "openminds.core.Affiliation",
            "^vocab:memberOf",
            reverse="member_of",
            multiple=True,
            doc="reverse of 'memberOf'",
        ),
        Property(
            "hosts",
            ["openminds.core.FileRepository", "openminds.publications.LivePaperResourceItem"],
            "^vocab:hostedBy",
            reverse="hosted_by",
            multiple=True,
            doc="reverse of 'hostedBy'",
        ),
        Property(
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
        Property(
            "is_owner_of",
            [
                "openminds.ephys.Electrode",
                "openminds.ephys.ElectrodeArray",
                "openminds.ephys.Pipette",
                "openminds.specimen_prep.SlicingDevice",
            ],
            "^vocab:owner",
            reverse="owners",
            multiple=True,
            doc="reverse of 'owner'",
        ),
        Property(
            "is_provider_of",
            "openminds.chemicals.ProductSource",
            "^vocab:provider",
            reverse="providers",
            multiple=True,
            doc="reverse of 'provider'",
        ),
        Property(
            "manufactured",
            "openminds.core.Setup",
            "^vocab:manufacturer",
            reverse="manufacturers",
            multiple=True,
            doc="reverse of 'manufacturer'",
        ),
        Property(
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
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("full_name",)

    def __init__(
        self,
        name=None,
        alias=None,
        affiliations=None,
        coordinated_projects=None,
        developed=None,
        digital_identifiers=None,
        full_name=None,
        funded=None,
        has_children=None,
        has_members=None,
        has_parents=None,
        homepage=None,
        hosts=None,
        is_custodian_of=None,
        is_owner_of=None,
        is_provider_of=None,
        manufactured=None,
        published=None,
        short_name=None,
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
            coordinated_projects=coordinated_projects,
            developed=developed,
            digital_identifiers=digital_identifiers,
            full_name=full_name,
            funded=funded,
            has_children=has_children,
            has_members=has_members,
            has_parents=has_parents,
            homepage=homepage,
            hosts=hosts,
            is_custodian_of=is_custodian_of,
            is_owner_of=is_owner_of,
            is_provider_of=is_provider_of,
            manufactured=manufactured,
            published=published,
            short_name=short_name,
        )
