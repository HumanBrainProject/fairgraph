"""
Structured information about a measurement performed during a scientific experiment.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


from datetime import datetime


class Measurement(EmbeddedMetadata):
    """
    Structured information about a measurement performed during a scientific experiment.
    """

    type_ = ["https://openminds.ebrains.eu/core/Measurement"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "additional_remarks",
            str,
            "vocab:additionalRemarks",
            doc="Mention of what deserves additional attention or notice.",
        ),
        Field(
            "measured_quantity",
            "openminds.controlledterms.MeasuredQuantity",
            "vocab:measuredQuantity",
            required=True,
            doc="no description available",
        ),
        Field(
            "measured_with",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimenprep.SlicingDeviceUsage",
            ],
            "vocab:measuredWith",
            doc="no description available",
        ),
        Field("timestamp", datetime, "vocab:timestamp", doc="no description available"),
        Field(
            "values",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:value",
            multiple=True,
            required=True,
            doc="Entry for a property.",
        ),
    ]

    def __init__(
        self,
        additional_remarks=None,
        measured_quantity=None,
        measured_with=None,
        timestamp=None,
        values=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            data=data,
            additional_remarks=additional_remarks,
            measured_quantity=measured_quantity,
            measured_with=measured_with,
            timestamp=timestamp,
            values=values,
        )
