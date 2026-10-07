"""
Structured information on a person.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Person as OMPerson
from fairgraph import KGObject


class Person(KGObject, OMPerson):
    """
    Structured information on a person.
    """

    type_ = "https://openminds.om-i.org/types/Person"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "activities",
            [
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.ephys.CellPatching",
                "openminds.v5.ephys.ElectrodePlacement",
                "openminds.v5.ephys.RecordingActivity",
                "openminds.v5.neuroimaging.DynamicMRIAcquisition",
                "openminds.v5.neuroimaging.StaticMRIAcquisition",
                "openminds.v5.specimen_prep.CranialWindowPreparation",
                "openminds.v5.specimen_prep.TissueCulturePreparation",
                "openminds.v5.specimen_prep.TissueSampleSlicing",
                "openminds.v5.stimulation.StimulationActivity",
            ],
            "performedBy",
            reverse="performed_by",
            multiple=True,
            description="reverse of 'performed_by'",
        ),
        Property(
            "authored",
            "openminds.v5.core.UsageAgreement",
            "authoringParty",
            reverse="authoring_parties",
            multiple=True,
            description="reverse of 'authoring_parties'",
        ),
        Property(
            "comments",
            "openminds.v5.core.Comment",
            "commenter",
            reverse="commenter",
            multiple=True,
            description="reverse of 'commenter'",
        ),
        Property(
            "contributed_to",
            [
                "openminds.v5.core.HardwareProduct",
                "openminds.v5.ephys.Electrode",
                "openminds.v5.ephys.ElectrodeArray",
                "openminds.v5.ephys.Pipette",
                "openminds.v5.neuroimaging.MRICoil",
                "openminds.v5.neuroimaging.MRIScanner",
                "openminds.v5.specimen_prep.SlicingDevice",
            ],
            "contribution",
            reverse="contributions",
            multiple=True,
            description="reverse of 'contributions'",
        ),
        Property(
            "funded",
            "openminds.v5.core.Funding",
            "funder",
            reverse="funder",
            multiple=True,
            description="reverse of 'funder'",
        ),
        Property(
            "is_member_of",
            "openminds.v5.core.Membership",
            "member",
            reverse="member",
            multiple=True,
            description="reverse of 'member'",
        ),
        Property(
            "is_provider_of",
            "openminds.v5.chemicals.ProductSource",
            "provider",
            reverse="provider",
            multiple=True,
            description="reverse of 'provider'",
        ),
        Property(
            "manufactured",
            "openminds.v5.core.Setup",
            "manufacturer",
            reverse="manufacturers",
            multiple=True,
            description="reverse of 'manufacturers'",
        ),
        Property(
            "started",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
                "openminds.v5.computation.WorkflowExecution",
            ],
            "startedBy",
            reverse="started_by",
            multiple=True,
            description="reverse of 'started_by'",
        ),
    ]
    existence_query_properties = ("given_name", "family_name")

    def __init__(
        self,
        activities=None,
        alternate_names=None,
        associated_accounts=None,
        authored=None,
        comments=None,
        contact_information=None,
        contributed_to=None,
        digital_identifiers=None,
        family_name=None,
        funded=None,
        given_name=None,
        is_member_of=None,
        is_provider_of=None,
        manufactured=None,
        preferred_name=None,
        started=None,
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
            activities=activities,
            alternate_names=alternate_names,
            associated_accounts=associated_accounts,
            authored=authored,
            comments=comments,
            contact_information=contact_information,
            contributed_to=contributed_to,
            digital_identifiers=digital_identifiers,
            family_name=family_name,
            funded=funded,
            given_name=given_name,
            is_member_of=is_member_of,
            is_provider_of=is_provider_of,
            manufactured=manufactured,
            preferred_name=preferred_name,
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
            release_status="in progress",
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
