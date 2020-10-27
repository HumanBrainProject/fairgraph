# encoding: utf-8
"""

"""

# Copyright 2018-2019 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import collections
try:
    basestring
except NameError:
    basestring = str
import requests
from .base import KGObject, KGProxy, OntologyTerm, StructuredMetadata, Field


class Address(StructuredMetadata):

    def __init__(self, locality, country):
        self.locality = locality
        self.country = country

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.locality!r}, {self.country!r})'.format(self=self))

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.locality == other.locality
                and self.country == other.country)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_jsonld(self, client=None):
        return {
            "@type": "schema:PostalAddress",
            "addressLocality": self.locality,
            "addressCountry": self.country
        }

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        if "addressLocality" in data:  # hack: need to fix URI handling properly
            return cls(data["addressLocality"], data["addressCountry"])
        else:
            return cls(data["http://schema.org/addressLocality"],
                       data["http://schema.org/addressCountry"])


class Group(OntologyTerm):
    """
    The subject group
    """
    iri_map = {
        "control group": "http://www.ontobee.org/ontology/NCIT?iri=http://purl.obolibrary.org/obo/NCIT_C28143",
        "treatment group": "http://www.ontobee.org/ontology/NCIT?iri=http://purl.obolibrary.org/obo/NCIT_C161322"
    }


class CultureType(OntologyTerm):
    """
    The type of cell culture used
    """
    iri_map = {
        "primary": "http://purl.obolibrary.org/obo/OBI_0001910",
        "secondary": "http://purl.obolibrary.org/obo/OBI_0001905",
        "cell line": "http://purl.obolibrary.org/obo/CLO_0000031"
    }


class Species(OntologyTerm):
    """
    The species of an experimental subject, expressed with the binomial nomenclature.
    """
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


class Shape(OntologyTerm):
    """
    Shape of a region of interest (ROI).
    """
    iri_map = {
        "circle": "https://en.wiktionary.org/wiki/circle",
        "ellipse": "https://en.wiktionary.org/wiki/ellipse",
	"freeform": "https://en.wiktionary.org/wiki/free-form#English",
        "rectangle": "https://en.wiktionary.org/wiki/rectangle",
        "square": "https://en.wiktionary.org/wiki/square"
    }


class MorphologyType(OntologyTerm):
    """
    The morphology of the cell used for recording.
    """
    iri_map = {
        "bipolar": "http://purl.obolibrary.org/obo/FMA_67282"
    }


class Strain(OntologyTerm):
    """
    An inbred sub-population within a species.
    """
    iri_map = {
        "129/Sv": "http://www.hbp.FIXME.org/hbp_strain_ontology/12345673",
        # 129/Sv is ambiguous
        # could be https://www.jax.org/strain/002448 or https://www.jax.org/strain/000691 or other
        # see http://www.informatics.jax.org/mgihome/nomen/strain_129.shtml
        #"Sprague-Dawley": "https://rgd.mcw.edu/rgdweb/report/strain/main.html?id=70508",
        "ATJ/FVB.129P2-FMR1-mix": "https://www.jax.org/strain/004624",
        "B6.129-Nlgn3<tm4Sud>/J": "https://www.jax.org/strain/023398",
        "B6.129-Nlgn3/J": "https://www.jax.org/strain/008475",
        "B6.129-Nlgn3/KftnkRbrc": "https://www.jax.org/strain/008475",
        "C57BL/6": "https://www.jax.org/strain/000664",
        "C57BL/6J": "https://www.jax.org/strain/000664",
        "C57BL6/SJL": "https://www.jax.org/strain/100012",
        "C57BL/6J-Tg(Thy1-GCaMP6f)GP5.5Dkim/J":"https://www.jax.org/strain/024276",
        "C57BL/6J X SJL": "http://www.hbp.FIXME.org/hbp_strain_ontology/12345672",
	    "Del(5Gtf2i-Fkbp6)1Vcam": "http://www.informatics.jax.org/allele/MGI:5555958",
        "Sprague-Dawley": "https://rgd.mcw.edu/rgdweb/ontology/view.html?acc_id=RS:0000681",
        "SWR": "http://www.informatics.jax.org/inbred_strains/mouse/docs/SWR.shtml",
        "Tg2576": "http://www.hbp.FIXME.org/hbp_strain_ontology/12345670",
        #"Wistar":  "https://rgd.mcw.edu/rgdweb/report/strain/main.html?id=13508588",
        "Wistar": "https://rgd.mcw.edu/rgdweb/ontology/view.html?acc_id=RS:0001013"
    }
# use RRIDs

class Genotype(OntologyTerm):
    """
    Transgenic modification of the strain.
    """
    iri_map = {
	    "wild type": "http://purl.obolibrary.org/obo/GENO_0000511",
	    "Fmr1KO": "https://www.jax.org/strain/003025",
        "GlyT2-GFP":"http://www.informatics.jax.org/allele/MGI:3835459",
        "IB2-KO": "http://www.hbp.FIXME.org/hbp_brain_region_ontology/1234567",
        "Nlgn3KO/Y; hemizygous": "http://www.informatics.jax.org/allele/MGI:5439278",
        "NL3R451C/Y; hemizygous": "http://www.informatics.jax.org/allele/MGI:3758949",
        "Tg(Thy1-GCaMP6f)GP5.17Dkim/J": "https://www.jax.org/strain/025393",
        "Cre/tdTomato": "https://www.jax.org/strain/007909",
        "C57BL/6J-Tg(Thy1-GCaMP6f)GP5.17Dkim/J": "https://www.jax.org/strain/025393"
    }


class Sex(OntologyTerm):
    """
    The sex of an animal or person from whom/which data were obtained.
    """
    iri_map = {
        "female": "schema:Female",
        "male": "schema:Male"
    }


class Handedness(OntologyTerm):
    """
    The handedness of an animal or person from whom/which data were obtained.
    """
    iri_map = {
        "left":"http://dbpedia.org/ontology/handedness",
        "right":"http://dbpedia.org/ontology/handedness"
    }

class ChannelType(OntologyTerm):
    """
    The handedness of an animal or person from whom/which data were obtained.
    """
    iri_map = {
        "ECoG":"http://purl.obolibrary.org/obo/NCIT_C116664",
	    "ECG": "http://purl.obolibrary.org/obo/NCIT_C38054",
        "EEG":"http://purl.obolibrary.org/obo/NCIT_C38054",
	    "EMG" : "http://purl.obolibrary.org/obo/NCIT_C38056",
        "ERP":"http://purl.bioontology.org/ontology/SNOMEDCT/251630008",
	    "MEG": "http://purl.obolibrary.org/obo/NCIT_C16811",
	    "SEEG": "https://en.wikipedia.org/wiki/Stereoelectroencephalography"
    }

class BrainRegion(OntologyTerm):
    """
    A sub-structure or region with the brain.
    """
    iri_map = {
        "anterolateral visual area": "http://purl.obolibrary.org/obo/UBERON_0035894",
        "anteromedial visual area": "http://purl.obolibrary.org/obo/UBERON_0035893",
        "basal ganglia": "http://purl.obolibrary.org/obo/UBERON_0010011",
        "brainstem": "http://purl.obolibrary.org/obo/UBERON_0002298",
        "CA3 field of hippocampus": "http://purl.obolibrary.org/obo/UBERON_0003883",
        "cerebellum": "http://purl.obolibrary.org/obo/UBERON_0002037",
        "cerebral cortex": "http://purl.obolibrary.org/obo/UBERON_0016529",
        "cortex": "http://purl.obolibrary.org/obo/UBERON_0016529",
        "dorsal cortex": "http://purl.obolibrary.org/obo/UBERON_0002577",
        "dorsal striatum": "http://purl.obolibrary.org/obo/UBERON_0005382",
	    "frontal association cortex": "http://purl.obolibrary.org/obo/UBERON_0000451",
        "hippocampus": "http://purl.obolibrary.org/obo/UBERON_0001954",  # Ammon's horn
        "hippocampus CA1": "http://purl.obolibrary.org/obo/UBERON_0003881",
        "hippocampal formation": "http://purl.obolibrary.org/obo/UBERON_0002421",
        "lobule 5 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004079",
        "lobule 6 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004080",
        "lobule 7 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004081",
        "lobule 8 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004082",
	    "motor cortex": "http://purl.obolibrary.org/obo/UBERON_0001384",
	    "parietal association area": "http://purl.obolibrary.org/obo/UBERON_0035886",
        "posteromedial visual area": "http://purl.obolibrary.org/obo/UBERON_0035900",
        "prefrontal cortex": "http://purl.obolibrary.org/obo/UBERON_0000451",
        "prelimbic cortex": "http://purl.obolibrary.org/obo/UBERON_0013560",
        "primary auditory cortex": "http://purl.obolibrary.org/obo/UBERON_0034751",
        "primary auditory cortex": "http://purl.obolibrary.org/obo/UBERON_0034751",
    	"primary motor cortex": "http://purl.obolibrary.org/obo/UBERON_0001384",
    	"primary somatosensory cortex": "http://purl.obolibrary.org/obo/UBERON_0008933",
    	"primary visual cortex": "http://purl.obolibrary.org/obo/UBERON_0002436",
        "retina": "http://purl.obolibrary.org/obo/UBERON_0000966",
    	"retrosplenial cortex": "http://purl.obolibrary.org/obo/UBERON_0013531",
    	"secondary motor cortex": "http://purl.obolibrary.org/obo/UBERON_0016634",
    	"secondary visual cortex": "http://purl.obolibrary.org/obo/UBERON_0022232",
        "somatosensory cortex": "http://purl.obolibrary.org/obo/UBERON_0008930",
        "spinal cord": "http://purl.obolibrary.org/obo/UBERON_0002240",
        "striatum": "http://purl.obolibrary.org/obo/UBERON_0002435",
        "thalamocortical": "http://www.hbp.FIXME.org/hbp_brain_region_ontology/1234567",
        "thalamus": "http://purl.obolibrary.org/obo/UBERON_0001897",
        "ventral hippocampus": "http://purl.obolibrary.org/obo/UBERON_0001954",   # how to distinguish this? Question for Tier 2 folks?
	    "visual cortex": "http://purl.obolibrary.org/obo/UBERON_0000411",
        "whole brain": "http://purl.obolibrary.org/obo/UBERON_0000955",
        "5th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004",
        # more specific term to be determined: http://purl.obolibrary.org/obo/UBERON_0024001 or http://purl.obolibrary.org/obo/UBERON_0004079 ?
        "6th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004",  # more specific term to be determined
        "7th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004",  # more specific term to be determined
        "8th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004004"  # more specific term to be determined
    }


class CellType(OntologyTerm):
    """A type of neuron or glial cell."""
    iri_map = {
        "cerebellar granule cell": "http://purl.obolibrary.org/obo/CL_0001031",
        "cholinergic interneuron": "http://uri.interlex.org/base/ilx_0490357",
        "fast spiking interneuron": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345670",
        "Golgi cell": "http://purl.obolibrary.org/obo/CL_0000119",
        "granule cell": "http://purl.obolibrary.org/obo/CL_0000120",
        "hippocampus CA1 basket cell": "http://uri.neuinfo.org/nif/nifstd/nlx_cell_091205",
        "hippocampus CA1 bistratified cell": "unknown",
        "hippocampus CA1 ivy neuron": "http://uri.neuinfo.org/nif/nifstd/nlx_35220",
        "hippocampus CA1 lacunosum moleculare neuron": "http://uri.neuinfo.org/nif/nifstd/nlx_92500",
        "hippocampus CA1 pyramidal cell": "http://uri.neuinfo.org/nif/nifstd/sao830368389",
        "hippocampus CA3 pyramidal cell": "http://uri.neuinfo.org/nif/nifstd/sao383526650",
        "hippocampus interneuron BP": "unknown",
        "interneuron": "http://purl.obolibrary.org/obo/CL_0000099",
        "medium spiny neuron": "http://purl.obolibrary.org/obo/CL_1001474",
        "medium spiny neuron (D1 type)": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345672",
        "medium spiny neuron (D2 type)": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345671",
        "not applicable": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345673",
        "Purkinje cell": "http://purl.obolibrary.org/obo/CL_0000121",
        "pyramidal cell": "http://purl.obolibrary.org/obo/CL_0000598",
        "spiny stellate neuron": "http://uri.neuinfo.org/nif/nifstd/sao1236796660",
        "L1 neurogliaform cell": "http://uri.interlex.org/base/ilx_0383196",
        "L2 inverted pyramidal cell": "http://uri.interlex.org/base/ilx_0383207",
        "L2/3 chandelier cell": "http://uri.interlex.org/base/ilx_0383200",
        "L2/3 pyramidal cell": "http://uri.neuinfo.org/nif/nifstd/nifext_49",
        "L4 Martinotti cell": "http://uri.neuinfo.org/nif/nifstd/nifext_55",
        "L5 pyramidal cell": "http://uri.interlex.org/ilx_0107385",
        "L5 tufted pyramidal cell": "http://uri.interlex.org/base/ilx_0738209",
        "L6 inverted pyramidal cell": "http://uri.interlex.org/base/ilx_0381373"
    }


class AbstractionLevel(OntologyTerm):
    """
    Level of abstraction for a neuroscience model, e.g.rate neurons, spiking neurons
    """
    iri_map = {
        "cognitive modelling": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345674",
        "population modelling": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345671",
        "population modelling: neural field": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345672",
        "population modelling: neural mass": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345673",
        "protein structure": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345670",
        "rate neurons": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000144",
        "systems biology": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000062",
        "systems biology: continuous": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000062",
        "systems biology: discrete": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000063",
        "systems biology: flux balance": "http://www.ebi.ac.uk/sbo/main/display?sboId=SBO:0000624",
        "spiking neurons": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000014",
        "spiking neurons: biophysical": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000017",
        "spiking neurons: point neuron": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000018",
        "rate neurons": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000144",
        "population modelling": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345671",
        "population modelling: neural field": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345672",
        "population modelling: neural mass": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345673",
        "cognitive modelling": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345674",
        "algorithm": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345675",
        "statistical model": "http://dbpedia.org/page/Statistical_model"
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
        "subcellular": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345675",
        "subcellular: ion channel": "http://uri.neuinfo.org/nif/nifstd/nifext_2508",
        "subcellular: molecular": "http://www.hbp.FIXME.org/hbp_modelling_ontology/12345676",
        "subcellular: signalling": "http://uri.interlex.org/base/ilx_0503639",  # "biochemical processes", not ideal
        "subcellular: spine": "http://uri.neuinfo.org/nif/nifstd/sao1145756102",
        "single cell": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000008",
        "network": "http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#cno_0000010",
        "network: brain region": "http://purl.obolibrary.org/obo/UBERON_0002616",
        "network: microcircuit":  "http://purl.obolibrary.org/obo/UBERON_0014778",  # "cell group", not ideal
        "network: whole brain": "http://purl.obolibrary.org/obo/UBERON_0000955"
    }


class License(OntologyTerm):
    iri_map = {
        "GNU General Public License 2 or later": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
        "CeCILL v2": "http://www.cecill.info/licences/Licence_CeCILL_V2-en.html"
    }

    @classmethod
    def initialize(cls):
        spdx_url = "https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json"
        response = requests.get(spdx_url)
        if response.status_code != 200:
            raise Exception("Unable to retrieve license list")
        license_data = response.json()
        for entry in license_data["licenses"]:
            cls.iri_map[entry["name"]] = entry["seeAlso"][0]


class StimulusType(OntologyTerm):
    iri_map = {
        "Excitatory postsynaptic currents": "http://ontologies.humanbrainproject.eu/ephys_stimuli/0001000",
	    "Excitatory postsynaptic potentials": "http://ontologies.humanbrainproject.eu/ephys_stimuli/0001000",
	    "Mossy Fiber Stimulation": "http://www.FIXME.org/ephys_stimuli/0000001",
        "No stimulus (spontaneous activity)": "http://www.FIXME.org/ephys_stimuli/0000000",
        "Pre-synaptic extracellular electrical stimulation": "http://www.FIXME.org/ephys_stimuli/0000001",
        "Sinusoidal current injections": "http://ontologies.humanbrainproject.eu/ephys_stimuli/0001000",
        "Step current": "http://www.FIXME.org/ephys_stimuli/0000001",
        "Unknown": "N/A"
    }


class Origin(OntologyTerm):
    iri_map = {
        "centre": "http://www.FIXME.org/ephys_stimuli/0000001",
        "bottom-left": "http://www.FIXME.org/ephys_stimuli/0000001",
        "top-right": "http://www.FIXME.org/ephys_stimuli/0000001"
    }


unit_codes = {
    "days": "http://purl.obolibrary.org/obo/UO_0000033",
    "weeks": "http://purl.obolibrary.org/obo/UO_0000034",
    "months": "http://purl.obolibrary.org/obo/UO_0000035",
    "years": "http://purl.obolibrary.org/obo/UO_0000036",
    "degrees": "http://purl.obolibrary.org/obo/UO_0000185",
    "µm": "http://purl.obolibrary.org/obo/UO_0000017",
    "mm": "http://purl.obolibrary.org/obo/UO_0000016",
    "nm": "http://purl.obolibrary.org/obo/UO_0000018",
    "mV": "http://purl.obolibrary.org/obo/UO_0000247",
    "ms": "http://purl.obolibrary.org/obo/UO_0000028",
    "s": "http://purl.obolibrary.org/obo/UO_0000010",
    "MΩ": "https://en.wiktionary.org/wiki/megaohm",
    "Mohm": "https://en.wiktionary.org/wiki/megaohm",
    "GΩ": "https://en.wiktionary.org/wiki/gigaohm",
    "Gohm": "https://en.wiktionary.org/wiki/gigaohm",
    "µA": "http://purl.obolibrary.org/obo/UO_0000038",
    "nA": "https://en.wiktionary.org/wiki/nanoamp",
    "Hz": "http://purl.obolibrary.org/obo/UO_0000106",
    "kHz": "http://purl.obolibrary.org/obo/NCIT_C67279"
}


class QuantitativeValue(StructuredMetadata):
    """docstring"""
    type = ("nsg:QuantitativeValue",)
    unit_codes = unit_codes

    def __init__(self, value, unit_text, unit_code=None):
        if not isinstance(value, (int, float)):
            raise ValueError("Must be a number")
        self.value = value
        self.unit_text = unit_text
        self.unit_code = unit_code or self.unit_codes[unit_text]

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.value!r} {self.unit_text!r})'.format(self=self))

    def __eq__(self, other):
        return (self.value == other.value
                and self.unit_text == other.unit_text
                and self.unit_code == other.unit_code)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_jsonld(self, client=None):
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
        for key in list(data):
            if "http://schema.org/" in key:
                data[key.replace("http://schema.org/", "")] = data[key]
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
        if "value" in data:
            return cls(float(data["value"]), unit_text, unit_code)
        elif "minValue" in data:
            return QuantitativeValueRange(float(data["minValue"]), float(data["maxValue"]),
                                          unit_text, unit_code)


class QuantitativeValueRange(StructuredMetadata):
    """docstring"""
    type = ("nsg:QuantitativeValueRange",)
    unit_codes = unit_codes

    def __init__(self, min, max, unit_text, unit_code=None):
        if not isinstance(min, (int, float)):
            raise ValueError("'min' must be a number")
        if not isinstance(max, (int, float)):
            raise ValueError("'max' must be a number")
        self.min = min
        self.max = max
        self.unit_text = unit_text
        self.unit_code = unit_code or self.unit_codes[unit_text]

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.min!r}-{self.max!r} {self.unit_text!r})'.format(self=self))

    def __eq__(self, other):
        return (self.min == other.min
                and self.max == other.max
                and self.unit_text == other.unit_text
                and self.unit_code == other.unit_code)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_jsonld(self, client=None):
        return {
            "@type": "nsg:QuantitativeValue",  # needs 'nsg:' prefix, no?
            "minValue": self.min,
            "maxValue": self.max,
            "label": self.unit_text,
            "unitCode": {"@id": self.unit_code}
        }

    def to_jsonld_alt(self):
        return {
            "minValue": self.min,
            "maxValue": self.max,
            "unitText": self.unit_text
        }

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        for key in list(data):
            if "http://schema.org/" in key:
                data[key.replace("http://schema.org/", "")] = data[key]
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
        return cls(float(data["minValue"]), data["maxValue"], unit_text, unit_code)


class Age(StructuredMetadata):
    allowed_periods = [
        "Pre-natal",
        "Post-natal"
    ]
    context = {
        "value": "http://schema.org/value",
        "period": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/period"
    }
    fields = (
        Field("value", basestring, "value", required=True),
        Field("period", basestring, "period", required=True, multiple=True)
    )

    def __init__(self, value, period):
        self.value = value
        if period not in Age.allowed_periods:
            raise ValueError("period must be one of {}".format(allowed_periods))
        self.period = period

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.value!r}, {self.period!r})'.format(self=self))

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.value == other.value
                and self.period == other.period)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_jsonld(self, client=None):
        return {'value': self.value.to_jsonld(),
                'period': self.period}

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        return cls(QuantitativeValue.from_jsonld(data["value"]), data["period"])
