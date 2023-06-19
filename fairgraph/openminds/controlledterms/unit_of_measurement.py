"""
Structured information on the unit of measurement.
    Here we show the first 20 possible values, an additional 32 values are not shown.

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - liter
         -
       * - millimolar
         - Millimolar is a decimal fraction of molar concentration that describes a solution as millimole per one liter of a solution.
       * - terabyte
         -
       * - degree Fahrenheit
         - The 'degree Fahrenheit' is a unit of temperature on the Fahrenheit scale where the freezing point of water is at 32 °F and the boiling point of water is at 212 °F under standard atmospheric pressure.
       * - milligram per milliliter
         -
       * - megaohm
         -
       * - nanoampere
         - An electric current unit current which is equal to one thousand millionth of an ampere or 10^[-9] A.
       * - second
         -
       * - `ampere <http://purl.obolibrary.org/obo/UO_0000011>`_
         - An electric current unit which is equal to the constant current which, if maintained in two straight parallel conductors of infinite length, of negligible circular cross-section, and placed 1 m apart in vacuum, would produce between these conductors a force equal to 2 x 10^[-7] newton per meter of length.
       * - degree Rankine
         - The 'degree Rankine' is a unit of temperature on the Rankine scale where the freezing point of water is at 491.67 °R and the boiling point of water is at 671.64102 °R under standard atmospheric pressure.
       * - microgram per milliliter
         -
       * - micromolar
         - Micromolar is a decimal fraction of molar concentration describing the amount of substance (measured in micromole) in one liter solution.
       * - degree Celsius
         - The 'degree Celsius' is a unit of temperature on the Celsius scale where the freezing point of water is at 0 °C and the boiling point of water is at 100 °C under standard atmospheric pressure.
       * - nanomolar
         - Nanomolar is a decimal fraction of molar concentration describing the amount of substance (measured in nanomole) in one liter solution.
       * - arcdegree
         - An arcdegree is a measurement of a plane angle in which one full rotation is 360 degrees.
       * - gigaohm
         -
       * - year
         -
       * - weight per volume percentage
         - Percentage of weight or mass of a dissolved, solid substance in a total volume of a solution. As per definition, the volume of a liquid is expressed in milliliter (ml) and the mass of a solute in grams (g)
       * - megabyte
         -
       * - molar
         - Molar is a measure of concentration that describes a solution as moles of solute per one liter of a solution.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class UnitOfMeasurement(KGObject):
    """
    Structured information on the unit of measurement.
    Here we show the first 20 possible values, an additional 32 values are not shown.

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - liter
         -
       * - millimolar
         - Millimolar is a decimal fraction of molar concentration that describes a solution as millimole per one liter of a solution.
       * - terabyte
         -
       * - degree Fahrenheit
         - The 'degree Fahrenheit' is a unit of temperature on the Fahrenheit scale where the freezing point of water is at 32 °F and the boiling point of water is at 212 °F under standard atmospheric pressure.
       * - milligram per milliliter
         -
       * - megaohm
         -
       * - nanoampere
         - An electric current unit current which is equal to one thousand millionth of an ampere or 10^[-9] A.
       * - second
         -
       * - `ampere <http://purl.obolibrary.org/obo/UO_0000011>`_
         - An electric current unit which is equal to the constant current which, if maintained in two straight parallel conductors of infinite length, of negligible circular cross-section, and placed 1 m apart in vacuum, would produce between these conductors a force equal to 2 x 10^[-7] newton per meter of length.
       * - degree Rankine
         - The 'degree Rankine' is a unit of temperature on the Rankine scale where the freezing point of water is at 491.67 °R and the boiling point of water is at 671.64102 °R under standard atmospheric pressure.
       * - microgram per milliliter
         -
       * - micromolar
         - Micromolar is a decimal fraction of molar concentration describing the amount of substance (measured in micromole) in one liter solution.
       * - degree Celsius
         - The 'degree Celsius' is a unit of temperature on the Celsius scale where the freezing point of water is at 0 °C and the boiling point of water is at 100 °C under standard atmospheric pressure.
       * - nanomolar
         - Nanomolar is a decimal fraction of molar concentration describing the amount of substance (measured in nanomole) in one liter solution.
       * - arcdegree
         - An arcdegree is a measurement of a plane angle in which one full rotation is 360 degrees.
       * - gigaohm
         -
       * - year
         -
       * - weight per volume percentage
         - Percentage of weight or mass of a dissolved, solid substance in a total volume of a solution. As per definition, the volume of a liquid is expressed in milliliter (ml) and the mass of a solute in grams (g)
       * - megabyte
         -
       * - molar
         - Molar is a measure of concentration that describes a solution as moles of solute per one liter of a solution.

    """

    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/UnitOfMeasurement"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the unit of measurement.",
        ),
        Field(
            "definition",
            str,
            "vocab:definition",
            doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the unit of measurement.",
        ),
        Field(
            "interlex_identifier",
            IRI,
            "vocab:interlexIdentifier",
            doc="Persistent identifier for a term registered in the InterLex project.",
        ),
        Field(
            "knowledge_space_link",
            IRI,
            "vocab:knowledgeSpaceLink",
            doc="Persistent link to an encyclopedia entry in the Knowledge Space project.",
        ),
        Field(
            "preferred_ontology_identifier",
            IRI,
            "vocab:preferredOntologyIdentifier",
            doc="Persistent identifier of a preferred ontological term.",
        ),
        Field(
            "synonyms",
            str,
            "vocab:synonym",
            multiple=True,
            doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses.",
        ),
        Field(
            "describes",
            [
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.DatasetVersion",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.ModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebServiceVersion",
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.LearningResource",
                "openminds.publications.LivePaperVersion",
                "openminds.publications.ScholarlyArticle",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:keyword",
            reverse="keywords",
            multiple=True,
            doc="reverse of 'keyword'",
        ),
        Field(
            "ranges",
            "openminds.core.QuantitativeValueRange",
            "^vocab:minValueUnit",
            reverse="min_value_units",
            multiple=True,
            doc="reverse of 'minValueUnit'",
        ),
        Field(
            "used_by",
            "openminds.sands.CustomCoordinateSpace",
            "^vocab:nativeUnit",
            reverse="native_units",
            multiple=True,
            doc="reverse of 'nativeUnit'",
        ),
        Field(
            "used_in",
            "openminds.ephys.Channel",
            "^vocab:unit",
            reverse="units",
            multiple=True,
            doc="reverse of 'unit'",
        ),
        Field(
            "values",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueArray"],
            "^vocab:unit",
            reverse="units",
            multiple=True,
            doc="reverse of 'unit'",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        definition=None,
        description=None,
        interlex_identifier=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        synonyms=None,
        describes=None,
        ranges=None,
        used_by=None,
        used_in=None,
        values=None,
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
            definition=definition,
            description=description,
            interlex_identifier=interlex_identifier,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
            describes=describes,
            ranges=ranges,
            used_by=used_by,
            used_in=used_in,
            values=values,
        )
