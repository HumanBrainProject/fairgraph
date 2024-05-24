"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class Strain(KGObject):
    """
    <description not available>
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/Strain"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "alternate_identifiers", str, "vocab:alternateIdentifier", multiple=True, doc="no description available"
        ),
        Property(
            "background_strains",
            "openminds.core.Strain",
            "vocab:backgroundStrain",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "breeding_type",
            "openminds.controlled_terms.BreedingType",
            "vocab:breedingType",
            doc="no description available",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the strain.",
        ),
        Property(
            "digital_identifier",
            "openminds.core.RRID",
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Property(
            "disease_models",
            ["openminds.controlled_terms.Disease", "openminds.controlled_terms.DiseaseModel"],
            "vocab:diseaseModel",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "genetic_strain_type",
            "openminds.controlled_terms.GeneticStrainType",
            "vocab:geneticStrainType",
            required=True,
            doc="no description available",
        ),
        Property("laboratory_code", str, "vocab:laboratoryCode", doc="no description available"),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the strain.",
        ),
        Property(
            "ontology_identifiers",
            str,
            "vocab:ontologyIdentifier",
            multiple=True,
            doc="Term or code used to identify the strain registered within a particular ontology.",
        ),
        Property("phenotype", str, "vocab:phenotype", doc="Physical expression of one or more genes of an organism."),
        Property(
            "species",
            "openminds.controlled_terms.Species",
            "vocab:species",
            required=True,
            doc="Category of biological classification comprising related organisms or populations potentially capable of interbreeding, and being designated by a binomial that consists of the name of a genus followed by a Latin or latinized uncapitalized noun or adjective.",
        ),
        Property("stock_number", "openminds.core.StockNumber", "vocab:stockNumber", doc="no description available"),
        Property(
            "synonyms",
            str,
            "vocab:synonym",
            multiple=True,
            doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses.",
        ),
    ]
    reverse_properties = [
        Property(
            "is_background_strain_of",
            "openminds.core.Strain",
            "^vocab:backgroundStrain",
            reverse="background_strains",
            multiple=True,
            doc="reverse of 'backgroundStrain'",
        ),
        Property(
            "is_species_of",
            [
                "openminds.core.Subject",
                "openminds.core.SubjectGroup",
                "openminds.core.TissueSample",
                "openminds.core.TissueSampleCollection",
            ],
            "^vocab:species",
            reverse="species",
            multiple=True,
            doc="reverse of 'species'",
        ),
    ]
    existence_query_properties = ("genetic_strain_type", "name", "species")

    def __init__(
        self,
        name=None,
        alternate_identifiers=None,
        background_strains=None,
        breeding_type=None,
        description=None,
        digital_identifier=None,
        disease_models=None,
        genetic_strain_type=None,
        is_background_strain_of=None,
        is_species_of=None,
        laboratory_code=None,
        ontology_identifiers=None,
        phenotype=None,
        species=None,
        stock_number=None,
        synonyms=None,
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
            alternate_identifiers=alternate_identifiers,
            background_strains=background_strains,
            breeding_type=breeding_type,
            description=description,
            digital_identifier=digital_identifier,
            disease_models=disease_models,
            genetic_strain_type=genetic_strain_type,
            is_background_strain_of=is_background_strain_of,
            is_species_of=is_species_of,
            laboratory_code=laboratory_code,
            ontology_identifiers=ontology_identifiers,
            phenotype=phenotype,
            species=species,
            stock_number=stock_number,
            synonyms=synonyms,
        )
