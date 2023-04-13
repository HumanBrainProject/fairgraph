"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field




class CustomAnnotation(EmbeddedMetadata):
    """

    """
    type_ = ["https://openminds.ebrains.eu/sands/CustomAnnotation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("anchor_points", "openminds.core.QuantitativeValue", "vocab:anchorPoint", multiple=True, required=False,
              doc="no description available"),
        Field("coordinate_space", ["openminds.sands.CommonCoordinateSpaceVersion", "openminds.sands.CustomCoordinateSpace"], "vocab:coordinateSpace", multiple=False, required=True,
              doc="Two or three dimensional geometric setting."),
        Field("criteria", "openminds.core.ProtocolExecution", "vocab:criteria", multiple=False, required=False,
              doc="Aspects or standards on which a judgement or decision is based."),
        Field("criteria_quality_type", "openminds.controlledterms.CriteriaQualityType", "vocab:criteriaQualityType", multiple=False, required=True,
              doc="Distinct class that defines how the judgement or decision was made for a particular criteria."),
        Field("criteria_type", "openminds.controlledterms.AnnotationCriteriaType", "vocab:criteriaType", multiple=False, required=True,
              doc="no description available"),
        Field("inspired_bys", "openminds.core.File", "vocab:inspiredBy", multiple=True, required=False,
              doc="Reference to an inspiring element."),
        Field("internal_identifier", str, "vocab:internalIdentifier", multiple=False, required=False,
              doc="Term or code that identifies the custom annotation within a particular product."),
        Field("laterality", "openminds.controlledterms.Laterality", "vocab:laterality", multiple=True, required=False,
              doc="Differentiation between a pair of lateral homologous parts of the body."),
        Field("preferred_visualization", "openminds.sands.ViewerSpecification", "vocab:preferredVisualization", multiple=False, required=False,
              doc="no description available"),
        Field("specification", ["openminds.core.File", "openminds.core.PropertyValueList"], "vocab:specification", multiple=False, required=False,
              doc="Detailed and precise presentation of, or proposal for something."),
        Field("type", "openminds.controlledterms.AnnotationType", "vocab:type", multiple=False, required=True,
              doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to."),

    ]

    def __init__(self, anchor_points=None, coordinate_space=None, criteria=None, criteria_quality_type=None, criteria_type=None, inspired_bys=None, internal_identifier=None, laterality=None, preferred_visualization=None, specification=None, type=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, anchor_points=anchor_points, coordinate_space=coordinate_space, criteria=criteria, criteria_quality_type=criteria_quality_type, criteria_type=criteria_type, inspired_bys=inspired_bys, internal_identifier=internal_identifier, laterality=laterality, preferred_visualization=preferred_visualization, specification=specification, type=type)