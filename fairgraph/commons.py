# encoding: utf-8
"""

"""

import collections
#from typing import NamedTuple
from .base import KGObject, KGProxy, OntologyTerm


#class Address(NamedTuple):
#    locality: str
#    country: str

Address = collections.namedtuple('Address', ['locality', 'country'])


class Species(OntologyTerm):
    """docstring"""
    iri_map = {
        "Rodentia": "http://purl.obolibrary.org/obo/NCBITaxon_9989",
        "Mus musculus": "http://purl.obolibrary.org/obo/NCBITaxon_10090",
        "Rattus norvegicus": "http://purl.obolibrary.org/obo/NCBITaxon_10116",
        "Rattus rattus": "http://purl.obolibrary.org/obo/NCBITaxon_10117",
        "Callithrix jacchus": "http://purl.obolibrary.org/obo/NCBITaxon_9483",
        "Homo sapiens": "http://purl.obolibrary.org/obo/NCBITaxon_9606",
        "Macaca mulatta": "http://purl.obolibrary.org/obo/NCBITaxon_9544",
        "Monodelphis domestica": "http://purl.obolibrary.org/obo/NCBITaxon_13616",
        "Ornithorhynchus anatinus": "http://purl.obolibrary.org/obo/NCBITaxon_9258"
    }


class Strain(OntologyTerm):
    """docstring"""
    iri_map = {
        "Tg2576": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "C57BL/6": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "C57BL/6J X SJL": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "C57BL/6J": "https://www.jax.org/strain/000664",  # RRID:IMSR_JAX:000664
        #"Sprague-Dawley": "https://rgd.mcw.edu/rgdweb/report/strain/main.html?id=70508",
        "Sprague-Dawley": "https://rgd.mcw.edu/rgdweb/ontology/view.html?acc_id=RS:0000681",
        #"Wistar":  "https://rgd.mcw.edu/rgdweb/report/strain/main.html?id=13508588",
        "Wistar": "https://rgd.mcw.edu/rgdweb/ontology/view.html?acc_id=RS:0001013",
        "129/Sv": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        # 129/Sv is ambiguous
        # could be https://www.jax.org/strain/002448 or https://www.jax.org/strain/000691 or other
        # see http://www.informatics.jax.org/mgihome/nomen/strain_129.shtml
    }
# use RRIDs


class Sex(OntologyTerm):
    """docstring"""
    iri_map = {
        "male": "schema:Male",
        "female": "schema:Female"
    }


class BrainRegion(OntologyTerm):
    """docstring"""
    iri_map = {
        "hippocampus CA1": "http://purl.obolibrary.org/obo/UBERON_0003881",
        "hippocampus": "http://purl.obolibrary.org/obo/UBERON_0001954",  # Ammon's horn
        "hippocampal formation": "http://purl.obolibrary.org/obo/UBERON_0002421",
        "ventral hippocampus": "http://purl.obolibrary.org/obo/UBERON_0001954",   # how to distinguish this? Question for Tier 2 folks?
        "somatosensory cortex": "http://purl.obolibrary.org/obo/UBERON_0008930",
        "thalamus": "http://purl.obolibrary.org/obo/UBERON_0001897",
        "brainstem": "http://purl.obolibrary.org/obo/UBERON_0002298",
        "spinal cord": "http://purl.obolibrary.org/obo/UBERON_0002240",
        "basal ganglia": "http://purl.obolibrary.org/obo/UBERON_0010011",
        "cortex": "http://purl.obolibrary.org/obo/UBERON_0016529",
        "cerebral cortex": "http://purl.obolibrary.org/obo/UBERON_0016529",
        "cerebellum": "http://purl.obolibrary.org/obo/UBERON_0002037",
        "whole brain": "http://purl.obolibrary.org/obo/UBERON_0000955",
        "striatum": "http://purl.obolibrary.org/obo/UBERON_0002435",
        "thalamocortical": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "5th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004",
        # more specific term to be determined: http://purl.obolibrary.org/obo/UBERON_0024001 or http://purl.obolibrary.org/obo/UBERON_0004079 ?
        "6th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004",  # more specific term to be determined
        "7th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004",  # more specific term to be determined
        "8th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004",  # more specific term to be determined
        "lobule 5 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004079",
        "lobule 6 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004080",
        "lobule 7 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004081",
        "lobule 8 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004082",
        "primary auditory cortex": "http://purl.obolibrary.org/obo/UBERON_0034751"
    }


class CellType(OntologyTerm):
    """docstring"""
    iri_map = {
        "hippocampus CA1 pyramidal cell": "http://uri.neuinfo.org/nif/nifstd/sao830368389",
        "hippocampus CA1 basket cell": "http://uri.neuinfo.org/nif/nifstd/nlx_cell_091205",
        "hippocampus interneuron BP": "unknown",
        "hippocampus CA1 bistratified cell": "unknown",
        "hippocampus CA1 lacunosum moleculare neuron": "http://uri.neuinfo.org/nif/nifstd/nlx_92500",
        "hippocampus CA1 ivy neuron": "http://uri.neuinfo.org/nif/nifstd/nlx_35220",
        "Purkinje cell": "http://purl.obolibrary.org/obo/CL_0000121",
        "medium spiny neuron": "http://purl.obolibrary.org/obo/CL_1001474",
        "interneuron": "http://purl.obolibrary.org/obo/CL_0000099",
        "Golgi cell": "http://purl.obolibrary.org/obo/CL_0000119",
        "pyramidal cell": "http://purl.obolibrary.org/obo/CL_0000598",
        "granule cell": "http://purl.obolibrary.org/obo/CL_0000120",
        "cerebellar granule cell": "http://purl.obolibrary.org/obo/CL_0001031",
        "L2/3 chandelier cell": "http://uri.interlex.org/base/ilx_0383200",
        "fast spiking interneuron": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "spiny stellate neuron": "http://uri.neuinfo.org/nif/nifstd/sao1236796660",
        "L5 tufted pyramidal cell": "http://uri.interlex.org/base/ilx_0738209",
        "L2/3 pyramidal cell": "http://uri.neuinfo.org/nif/nifstd/nifext_49",
        "medium spiny neuron (D2 type)": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "L6 inverted pyramidal cell": "http://uri.interlex.org/base/ilx_0381373",
        "L4 Martinotti cell": "http://uri.neuinfo.org/nif/nifstd/nifext_55",
        "medium spiny neuron (D1 type)": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "cholinergic interneuron": "http://uri.interlex.org/base/ilx_0490357",
        "L1 neurogliaform cell": "http://uri.interlex.org/base/ilx_0383196",
        "L2 inverted pyramidal cell": "http://uri.interlex.org/base/ilx_0383207",
        "not applicable": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567"
    }


class AbstractionLevel(OntologyTerm):
    """docstring"""
    iri_map = {
        "protein structure": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "systems biology": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000062",
        "systems biology: continuous": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000062",
        "systems biology: discrete": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000063",
        "systems biology: flux balance": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000624",
        "spiking neurons": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000014",
        "spiking neurons: biophysical": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000017",
        "spiking neurons: point neuron": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000018",
        "rate neurons": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000144",
        "population modelling": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "population modelling: neural field": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "population modelling: neural mass": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567",
        "cognitive modelling": "http://www.hbp.FIXME.org/hbp_taxonomy_ontology/1234567"
    }


# CNO model types
# 'cellular model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000008"
#     'artificial neuron model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000012"
#     'point process model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000013"
#     'rate-based neuron model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000144"
#     'spiking model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000014"
#         'biophysical spiking model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000017"
#             'detailed model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000020"
#             'reduced model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000019"
#         'threshold-based spiking model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000018"
#             'one variable model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000022"
#             'pulse-based model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000021"
#             'spike response model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000025"
#             'three variable model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000024"
#             'two variable model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000023"
# 'network model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000010"
#     'artificial neural network model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000029"
#     'rate model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000028"
#     'spiking network model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000030"
# 'plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000011"
#     'cellular plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000033"
#     'developmental plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000161"
#     'synaptic plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000034"
#         'homeostatic plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000187"
#         'long term plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000183"
#             'biophysical model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000186"
#             'phenomenological plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000007"
#                 'rate-based plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000184"
#                 'spike timing dependent plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000185"
#         'short term plasticity model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000182"
#             'short term depression model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000201"
#             'short term facilitation model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000035"
# 'synapse model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000009"
#     'chemical synapse model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000031"
#         'conductance-based model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000027"
#         'current-based model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000026"
#     'electrical synapse model' "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000026"


class ModelScope(OntologyTerm):
    """docstring"""
    iri_map = {
        "subcellular": "TODO",
        "subcellular: spine": "http://uri.neuinfo.org/nif/nifstd/sao1145756102",
        "subcellular: ion channel": "http://uri.neuinfo.org/nif/nifstd/nifext_2508",
        "subcellular: signalling": "http://uri.interlex.org/base/ilx_0503639",  # "biochemical processes", not ideal
        "subcellular: molecular": "TODO",
        "single cell": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000008",
        "network": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000010",
        "network: microcircuit":  "http://purl.obolibrary.org/obo/UBERON_0014778",  # "cell group", not ideal
        "network: brain region": "http://purl.obolibrary.org/obo/UBERON_0002616",
        "network: whole brain": "http://purl.obolibrary.org/obo/UBERON_0000955"
    }


class License(OntologyTerm):
    iri_map = {
        "GNU General Public License 2 or later": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
        "CeCILL v2": "http://www.cecill.info/licences/Licence_CeCILL_V2-en.html"
    }


class QuantitativeValue(object):
    """docstring"""
    unit_codes = {
        "days": "http://purl.obolibrary.org/obo/UO_0000033",
        "weeks": "http://purl.obolibrary.org/obo/UO_0000034",
        "months": "http://purl.obolibrary.org/obo/UO_0000035",
        "degrees": "http://purl.obolibrary.org/obo/UO_0000185",
        "µm": "http://purl.obolibrary.org/obo/UO_0000017",
        "mV":  "http://purl.obolibrary.org/obo/UO_0000247",
        "ms": "http://purl.obolibrary.org/obo/UO_0000028",
    }

    def __init__(self, value, unit_text, unit_code=None):
        if not isinstance(value, (int, float)):
            raise ValueError("Must be a number")
        self.value = value
        self.unit_text = unit_text
        self.unit_code = unit_code or self.unit_codes[unit_text]

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.value!r} {self.unit_text!r})')
        return ('{self.__class__.__name__}('
                '{self.value!r} {self.unit_text!r})'.format(self=self))

    def to_jsonld(self):
        return {
            "@type": "nsg:QuantitativeValue",  # needs 'nsg:' prefix, no?
            "value": self.value,
            "label": self.unit_text,
            "unitCode": {"@id": self.unit_code}
        }

    def to_jsonld_alt(self):
        return {
            "value": self.value,
            "unitText": self.unit_text
        }

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        if "label" in data:
            unit_text = data["label"]
        elif "unitText" in data:
            unit_text = data["unitText"]
        else:
            unit_text = "?"
        if "unitCode" in data:
            unit_code = data["unitCode"]["@id"]
        else:
            unit_code = None
        return cls(float(data["value"]), unit_text, unit_code)


class Age(object):

    def __init__(self, value, period):
        self.value = value
        self.period = period

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.value!r}, {self.period!r})')
        return ('{self.__class__.__name__}('
                '{self.value!r}, {self.period!r})'.format(self=self))

    def to_jsonld(self):
        return {'value': self.value.to_jsonld(),
                'period': self.period}

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        return cls(QuantitativeValue.from_jsonld(data["value"]), data["period"])
