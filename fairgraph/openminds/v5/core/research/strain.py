"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Strain as OMStrain
from fairgraph import KGObject


class Strain(KGObject, OMStrain):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Strain"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_background_strain_of",
            "openminds.v5.core.Strain",
            "backgroundStrain",
            reverse="background_strains",
            multiple=True,
            description="reverse of 'background_strains'",
        ),
        Property(
            "is_species_of",
            [
                "openminds.v5.core.Subject",
                "openminds.v5.core.SubjectGroup",
                "openminds.v5.core.TissueSample",
                "openminds.v5.core.TissueSampleCollection",
            ],
            "species",
            reverse="species",
            multiple=True,
            description="reverse of 'species'",
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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
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
