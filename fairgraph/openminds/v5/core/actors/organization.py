"""
An entity comprised of one or more natural persons with a particular purpose. [adapted from Wikipedia](https://en.wikipedia.org/wiki/Organization)
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Organization as OMOrganization
from fairgraph import KGObject


from openminds import IRI


class Organization(KGObject, OMOrganization):
    """
    An entity comprised of one or more natural persons with a particular purpose. [adapted from Wikipedia](https://en.wikipedia.org/wiki/Organization)
    """

    type_ = "https://openminds.om-i.org/types/Organization"
    default_space = "common"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "authored",
            "openminds.v5.core.UsageAgreement",
            "authoringParty",
            reverse="authoring_parties",
            multiple=True,
            description="reverse of 'authoring_parties'",
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
            "emitted",
            "openminds.v5.core.GenericIdentifier",
            "emitter",
            reverse="emitter",
            multiple=True,
            description="reverse of 'emitter'",
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
            "has_children",
            "openminds.v5.core.Organization",
            "hasParent",
            reverse="has_parents",
            multiple=True,
            description="reverse of 'has_parents'",
        ),
        Property(
            "hosts",
            ["openminds.v5.core.FileRepository", "openminds.v5.publications.LivePaperResourceItem"],
            "hostedBy",
            reverse="hosted_by",
            multiple=True,
            description="reverse of 'hosted_by'",
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
    ]
    existence_query_properties = ("country_of_formation", "name", "type")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        acronym=None,
        alternate_names=None,
        authored=None,
        contributed_to=None,
        country_of_formation=None,
        digital_identifiers=None,
        emitted=None,
        funded=None,
        has_children=None,
        has_parents=None,
        homepage=None,
        hosts=None,
        is_member_of=None,
        is_provider_of=None,
        jurisdiction=None,
        location=None,
        manufactured=None,
        memberships=None,
        type=None,
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
            acronym=acronym,
            alternate_names=alternate_names,
            authored=authored,
            contributed_to=contributed_to,
            country_of_formation=country_of_formation,
            digital_identifiers=digital_identifiers,
            emitted=emitted,
            funded=funded,
            has_children=has_children,
            has_parents=has_parents,
            homepage=homepage,
            hosts=hosts,
            is_member_of=is_member_of,
            is_provider_of=is_provider_of,
            jurisdiction=jurisdiction,
            location=location,
            manufactured=manufactured,
            memberships=memberships,
            type=type,
        )
