"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Service as OMService
from fairgraph import KGObject


class Service(KGObject, OMService):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Service"
    default_space = "software"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "deployments",
            "openminds.v5.computation.ServiceDeployment",
            "service",
            reverse="service",
            multiple=True,
            description="reverse of 'service'",
        ),
        Property(
            "has_accounts",
            "openminds.v5.core.AccountInformation",
            "service",
            reverse="service",
            multiple=True,
            description="reverse of 'service'",
        ),
        Property(
            "hosts",
            "openminds.v5.publications.LivePaperResourceItem",
            "hostedBy",
            reverse="hosted_by",
            multiple=True,
            description="reverse of 'hosted_by'",
        ),
        Property(
            "used_for",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
            ],
            "environment",
            reverse="environment",
            multiple=True,
            description="reverse of 'environment'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("short_name",)

    def __init__(
        self,
        name=None,
        alias=None,
        contributions=None,
        deployments=None,
        description=None,
        documentation=None,
        full_name=None,
        has_accounts=None,
        hosts=None,
        how_to_cite=None,
        keywords=None,
        related_publications=None,
        scopes=None,
        short_name=None,
        support_channels=None,
        used_for=None,
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
            contributions=contributions,
            deployments=deployments,
            description=description,
            documentation=documentation,
            full_name=full_name,
            has_accounts=has_accounts,
            hosts=hosts,
            how_to_cite=how_to_cite,
            keywords=keywords,
            related_publications=related_publications,
            scopes=scopes,
            short_name=short_name,
            support_channels=support_channels,
            used_for=used_for,
        )
