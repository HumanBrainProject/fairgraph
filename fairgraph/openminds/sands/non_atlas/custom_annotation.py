"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class CustomAnnotation(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = "https://openminds.ebrains.eu/sands/CustomAnnotation"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "anchor_points",
            "openminds.core.QuantitativeValue",
            "vocab:anchorPoint",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "coordinate_space",
            ["openminds.sands.CommonCoordinateSpaceVersion", "openminds.sands.CustomCoordinateSpace"],
            "vocab:coordinateSpace",
            required=True,
            doc="Two or three dimensional geometric setting.",
        ),
        Property(
            "criteria",
            "openminds.core.ProtocolExecution",
            "vocab:criteria",
            doc="Aspects or standards on which a judgement or decision is based.",
        ),
        Property(
            "criteria_quality_type",
            "openminds.controlled_terms.CriteriaQualityType",
            "vocab:criteriaQualityType",
            required=True,
            doc="Distinct class that defines how the judgement or decision was made for a particular criteria.",
        ),
        Property(
            "criteria_type",
            "openminds.controlled_terms.AnnotationCriteriaType",
            "vocab:criteriaType",
            required=True,
            doc="no description available",
        ),
        Property(
            "inspired_by",
            "openminds.core.File",
            "vocab:inspiredBy",
            multiple=True,
            doc="Reference to an inspiring element.",
        ),
        Property(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the custom annotation within a particular product.",
        ),
        Property(
            "lateralities",
            "openminds.controlled_terms.Laterality",
            "vocab:laterality",
            multiple=True,
            doc="Differentiation between a pair of lateral homologous parts of the body.",
        ),
        Property(
            "preferred_visualization",
            "openminds.sands.ViewerSpecification",
            "vocab:preferredVisualization",
            doc="no description available",
        ),
        Property(
            "specification",
            ["openminds.core.File", "openminds.core.PropertyValueList"],
            "vocab:specification",
            doc="Detailed and precise presentation of, or proposal for something.",
        ),
        Property(
            "type",
            "openminds.controlled_terms.AnnotationType",
            "vocab:type",
            required=True,
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
    ]
    reverse_properties = []

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
