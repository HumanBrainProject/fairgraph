"""
An entity comprised of one or more natural persons with a particular purpose. [adapted from Wikipedia](https://en.wikipedia.org/wiki/Organization)
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Organization as OMOrganization
from fairgraph import KGObject


from openminds import IRI


class Organization(KGObject, OMOrganization):
    """
    An entity comprised of one or more natural persons with a particular purpose. [adapted from Wikipedia](https://en.wikipedia.org/wiki/Organization)
    """

    type_ = "https://openminds.om-i.org/types/Organization"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "coordinated_projects",
            "openminds.v4.core.Project",
            "coordinator",
            reverse="coordinators",
            multiple=True,
            description="reverse of 'coordinators'",
        ),
        Property(
            "developed",
            [
                "openminds.v4.computation.ValidationTest",
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipe",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.MetaDataModel",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.Model",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.Software",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebService",
                "openminds.v4.core.WebServiceVersion",
            ],
            "developer",
            reverse="developers",
            multiple=True,
            description="reverse of 'developers'",
        ),
        Property(
            "funded",
            "openminds.v4.core.Funding",
            "funder",
            reverse="funder",
            multiple=True,
            description="reverse of 'funder'",
        ),
        Property(
            "has_children",
            "openminds.v4.core.Organization",
            "hasParent",
            reverse="has_parents",
            multiple=True,
            description="reverse of 'has_parents'",
        ),
        Property(
            "has_members",
            "openminds.v4.core.Affiliation",
            "memberOf",
            reverse="member_of",
            multiple=True,
            description="reverse of 'member_of'",
        ),
        Property(
            "hosts",
            ["openminds.v4.core.FileRepository", "openminds.v4.publications.LivePaperResourceItem"],
            "hostedBy",
            reverse="hosted_by",
            multiple=True,
            description="reverse of 'hosted_by'",
        ),
        Property(
            "is_custodian_of",
            [
                "openminds.v4.core.Dataset",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.publications.LivePaper",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.sands.BrainAtlas",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpace",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "custodian",
            reverse="custodians",
            multiple=True,
            description="reverse of 'custodians'",
        ),
        Property(
            "is_owner_of",
            [
                "openminds.v4.ephys.Electrode",
                "openminds.v4.ephys.ElectrodeArray",
                "openminds.v4.ephys.Pipette",
                "openminds.v4.specimen_prep.SlicingDevice",
            ],
            "owner",
            reverse="owners",
            multiple=True,
            description="reverse of 'owners'",
        ),
        Property(
            "is_provider_of",
            "openminds.v4.chemicals.ProductSource",
            "provider",
            reverse="provider",
            multiple=True,
            description="reverse of 'provider'",
        ),
        Property(
            "manufactured",
            "openminds.v4.core.Setup",
            "manufacturer",
            reverse="manufacturers",
            multiple=True,
            description="reverse of 'manufacturers'",
        ),
        Property(
            "published",
            [
                "openminds.v4.publications.Book",
                "openminds.v4.publications.Chapter",
                "openminds.v4.publications.LearningResource",
                "openminds.v4.publications.ScholarlyArticle",
            ],
            "publisher",
            reverse="publisher",
            multiple=True,
            description="reverse of 'publisher'",
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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
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
