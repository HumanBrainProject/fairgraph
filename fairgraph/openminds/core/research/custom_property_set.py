"""
Structured information about properties of an entity that cannot be represented with a more general openMINDS schema.
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base import EmbeddedMetadata, IRI
from fairgraph.fields import Field




class CustomPropertySet(EmbeddedMetadata):
    """
    Structured information about properties of an entity that cannot be represented with a more general openMINDS schema.
    """
    type = ["https://openminds.ebrains.eu/core/CustomPropertySet"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("context", str, "vocab:context", multiple=False, required=True,
              doc="no description available"),
        Field("data_location", ["openminds.core.Configuration", "openminds.core.File", "openminds.core.PropertyValueList"], "vocab:dataLocation", multiple=False, required=True,
              doc="no description available"),
        Field("relevant_for", ["openminds.controlledterms.AnalysisTechnique", "openminds.controlledterms.StimulationApproach", "openminds.controlledterms.StimulationTechnique", "openminds.controlledterms.Technique"], "vocab:relevantFor", multiple=False, required=True,
              doc="Reference to what or whom the custom property set bears siginificance."),

    ]
