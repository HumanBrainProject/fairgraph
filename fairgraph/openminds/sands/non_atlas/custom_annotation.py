"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class CustomAnnotation(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = ["https://openminds.ebrains.eu/sands/CustomAnnotation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "anchor_points",
            "openminds.core.QuantitativeValue",
            "vocab:anchorPoint",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "coordinate_space",
            ["openminds.sands.CommonCoordinateSpaceVersion", "openminds.sands.CustomCoordinateSpace"],
            "vocab:coordinateSpace",
            required=True,
            doc="Two or three dimensional geometric setting.",
        ),
        Field(
            "criteria",
            "openminds.core.ProtocolExecution",
            "vocab:criteria",
            doc="Aspects or standards on which a judgement or decision is based.",
        ),
        Field(
            "criteria_quality_type",
            "openminds.controlledterms.CriteriaQualityType",
            "vocab:criteriaQualityType",
            required=True,
            doc="Distinct class that defines how the judgement or decision was made for a particular criteria.",
        ),
        Field(
            "criteria_type",
            "openminds.controlledterms.AnnotationCriteriaType",
            "vocab:criteriaType",
            required=True,
            doc="no description available",
        ),
        Field(
            "inspired_by",
            "openminds.core.File",
            "vocab:inspiredBy",
            multiple=True,
            doc="Reference to an inspiring element.",
        ),
        Field(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the custom annotation within a particular product.",
        ),
        Field(
            "lateralities",
            "openminds.controlledterms.Laterality",
            "vocab:laterality",
            multiple=True,
            doc="Differentiation between a pair of lateral homologous parts of the body.",
        ),
        Field(
            "preferred_visualization",
            "openminds.sands.ViewerSpecification",
            "vocab:preferredVisualization",
            doc="no description available",
        ),
        Field(
            "specification",
            ["openminds.core.File", "openminds.core.PropertyValueList"],
            "vocab:specification",
            doc="Detailed and precise presentation of, or proposal for something.",
        ),
        Field(
            "type",
            "openminds.controlledterms.AnnotationType",
            "vocab:type",
            required=True,
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
    ]

    def __init__(
        self,
        anchor_points=None,
        coordinate_space=None,
        criteria=None,
        criteria_quality_type=None,
        criteria_type=None,
        inspired_by=None,
        internal_identifier=None,
        lateralities=None,
        preferred_visualization=None,
        specification=None,
        type=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            data=data,
            anchor_points=anchor_points,
            coordinate_space=coordinate_space,
            criteria=criteria,
            criteria_quality_type=criteria_quality_type,
            criteria_type=criteria_type,
            inspired_by=inspired_by,
            internal_identifier=internal_identifier,
            lateralities=lateralities,
            preferred_visualization=preferred_visualization,
            specification=specification,
            type=type,
        )
