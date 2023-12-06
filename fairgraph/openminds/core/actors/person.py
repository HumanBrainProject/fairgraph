"""
Structured information on a person.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class Person(KGObject):
    """
    Structured information on a person.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/Person"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "affiliations",
            "openminds.core.Affiliation",
            "vocab:affiliation",
            multiple=True,
            doc="Declaration of a person being closely associated to an organization.",
        ),
        Field("alternate_names", str, "vocab:alternateName", multiple=True, doc="no description available"),
        Field(
            "associated_accounts",
            "openminds.core.AccountInformation",
            "vocab:associatedAccount",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "contact_information",
            "openminds.core.ContactInformation",
            "vocab:contactInformation",
            doc="Any available way used to contact a person or business (e.g., address, phone number, email address, etc.).",
        ),
        Field(
            "digital_identifiers",
            "openminds.core.ORCID",
            "vocab:digitalIdentifier",
            multiple=True,
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field("family_name", str, "vocab:familyName", doc="Name borne in common by members of a family."),
        Field(
            "given_name",
            str,
            "vocab:givenName",
            required=True,
            doc="Name given to a person, including all potential middle names, but excluding the family name.",
        ),
        Field(
            "activities",
            [
                "openminds.core.ProtocolExecution",
                "openminds.ephys.CellPatching",
                "openminds.ephys.ElectrodePlacement",
                "openminds.ephys.RecordingActivity",
                "openminds.specimenprep.CranialWindowPreparation",
                "openminds.specimenprep.TissueCulturePreparation",
                "openminds.specimenprep.TissueSampleSlicing",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:performedBy",
            reverse="performed_by",
            multiple=True,
            doc="reverse of 'performedBy'",
        ),
        Field(
            "comments",
            "openminds.core.Comment",
            "^vocab:commenter",
            reverse="commenters",
            multiple=True,
            doc="reverse of 'commenter'",
        ),
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
        Field(
            "started",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
                "openminds.computation.WorkflowExecution",
            ],
            "^vocab:startedBy",
            reverse="started_by",
            multiple=True,
            doc="reverse of 'startedBy'",
        ),
    ]
    existence_query_fields = ("given_name", "family_name")

    def __init__(
        self,
        affiliations=None,
        alternate_names=None,
        associated_accounts=None,
        contact_information=None,
        digital_identifiers=None,
        family_name=None,
        given_name=None,
        activities=None,
        comments=None,
        coordinated_projects=None,
        developed=None,
        funded=None,
        is_custodian_of=None,
        is_owner_of=None,
        is_provider_of=None,
        manufactured=None,
        published=None,
        started=None,
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
            affiliations=affiliations,
            alternate_names=alternate_names,
            associated_accounts=associated_accounts,
            contact_information=contact_information,
            digital_identifiers=digital_identifiers,
            family_name=family_name,
            given_name=given_name,
            activities=activities,
            comments=comments,
            coordinated_projects=coordinated_projects,
            developed=developed,
            funded=funded,
            is_custodian_of=is_custodian_of,
            is_owner_of=is_owner_of,
            is_provider_of=is_provider_of,
            manufactured=manufactured,
            published=published,
            started=started,
        )

    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}"

    @classmethod
    def me(cls, client, allow_multiple=False, follow_links=None):
        user_info = client.user_info()
        possible_matches = cls.list(
            client,
            scope="in progress",
            space="common",
            follow_links=follow_links,
            family_name=user_info.family_name,
            given_name=user_info.given_name,
        )
        if len(possible_matches) == 0:
            person = Person(family_name=user_info.family_name, given_name=user_info.given_name)
        elif len(possible_matches) == 1:
            person = possible_matches[0]
        elif allow_multiple:
            person = possible_matches
        else:
            raise Exception("Found multiple matches")
        return person
