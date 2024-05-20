"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class Setup(KGObject):
    """
    <description not available>
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/Setup"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the setup.",
        ),
        Property(
            "has_parts",
            [
                "openminds.core.Setup",
                "openminds.core.SoftwareVersion",
                "openminds.ephys.Electrode",
                "openminds.ephys.ElectrodeArray",
                "openminds.ephys.Pipette",
                "openminds.specimen_prep.SlicingDevice",
            ],
            "vocab:hasPart",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Property("location", str, "vocab:location", doc="no description available"),
        Property(
            "manufacturers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:manufacturer",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the setup.",
        ),
        Property(
            "types",
            "openminds.controlled_terms.SetupType",
            "vocab:type",
            multiple=True,
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
        Property(
            "is_part_of",
            "openminds.core.Setup",
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Property(
            "used_in",
            "openminds.stimulation.StimulationActivity",
            "^vocab:setup",
            reverse="setups",
            multiple=True,
            doc="reverse of 'setup'",
        ),
    ]
    existence_query_properties = ("description", "has_parts", "name")

    def __init__(
        self,
        name=None,
        description=None,
        has_parts=None,
        is_part_of=None,
        location=None,
        manufacturers=None,
        types=None,
        used_in=None,
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
            description=description,
            has_parts=has_parts,
            is_part_of=is_part_of,
            location=location,
            manufacturers=manufacturers,
            types=types,
            used_in=used_in,
        )
