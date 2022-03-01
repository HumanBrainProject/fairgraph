# encoding: utf-8
"""

"""

# Copyright 2018-2020 CNRS

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
import logging
import json
from .base import OntologyTerm, StructuredMetadata
from .fields import Field

import requests
from .base import KGObject, KGProxy, OntologyTerm, StructuredMetadata

logger = logging.getLogger("fairgraph")


class Address(StructuredMetadata):

    def __init__(self, locality, country):
        self.locality = locality
        self.country = country

    def __repr__(self):
        return (f'{self.__class__.__name__}({self.locality!r}, {self.country!r})')

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
    # problem that the iri_map clashes with CellType iri_map
    # so need to improve iri-lookup
    iri_map = {
        "bipolar": "http://purl.obolibrary.org/obo/FMA_67282",
        #"pyramidal cell": "http://uri.interlex.org/ilx_0107385"
    }


class SomaType(OntologyTerm):
    """
    The type of soma of a reconstructed cell.
    """
    iri_map = {
        "3D": "http://www.hbp.FIXME.org/",
        "2D contour": "http://www.hbp.FIXME.org/",
        "1 point": "http://www.hbp.FIXME.org/",
        "3 point": "http://www.hbp.FIXME.org/"
    }


class ObjectiveType(OntologyTerm):
    """
    The type of objective used for microscopy.
    """
    iri_map = {
        "dry": "http://www.hbp.FIXME.org/",
        "oil": "http://www.hbp.FIXME.org/",
        "water": "http://www.hbp.FIXME.org/"
    }


class Strain(OntologyTerm):
    """
    An inbred sub-population within a species.
    """
    iri_map = {
        "129/Sv": "https://dknet.org/data/record/nlx_154697-1/MGI:5656185/resolver?q=129%2FSv&l=129%2FSv&i=5d422cf50fbc3b6016f5437e",
        # 129/Sv is ambiguous
        # could be https://www.jax.org/strain/002448 or https://www.jax.org/strain/000691 or other
        # see http://www.informatics.jax.org/mgihome/nomen/strain_129.shtml
        #"Sprague-Dawley": "https://rgd.mcw.edu/rgdweb/report/strain/main.html?id=70508",
        "ATJ/FVB.129P2-FMR1-mix": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:004624/resolver?q=%2A&l=&filter[]=Catalog%20Number:004624&i=5d422ff90fbc3b6016f6f089",
        "B6.129-Nlgn3<tm4Sud>/J": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:023398/resolver?q=%2A&l=&filter[]=Catalog%20Number:023398&i=5d42266e0fbc3b6016f1c113",
        "B6.129-Nlgn3/J": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:008475/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:008475&i=5d422c170fbc3b6016f4cb08",
        "B6.129-Nlgn3/KftnkRbrc": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:008475/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:008475&i=5d422c170fbc3b6016f4cb08",
        "BAC_cck/dsred//BAC_pva/gfp (TgTg) - FVB/AntF1": "http://www.hbp.FIXME.org/",
        "BAC_cck/dsred on FVB/ANT":"http://www.hbp.FIXME.org/",
        "BAC_PV/eGFP on FVB/ANT": "http://www.hbp.FIXME.org/",
        "BAC_PV/eGFP onFVB/ANT": "http://www.hbp.FIXME.org/",
        "BAC_pva/gfp (2) - FVB/AntFx": "http://www.hbp.FIXME.org/",
        "Bl6": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:000664/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:000664&i=5d4227790fbc3b6016f250e8",
        "C57BL/6": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:000664/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:000664&i=5d4227790fbc3b6016f250e8",
        "C57BL/6J": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:000664/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:000664&i=5d4227790fbc3b6016f250e8",
        "C57Bl/6J": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:000664/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:000664&i=5d4227790fbc3b6016f250e8",
        "C57BL6/SJL": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:100012/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:100012&i=5d422f510fbc3b6016f6939a",
        "C57BL/6J-Tg(Thy1-GCaMP6f)GP5.5Dkim/J":"https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:024276/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:024276&i=5d4232230fbc3b6016f81e3a",
        "C57BL/6J X SJL": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:100012/resolver?q=%2A&l=&filter[]=Catalog%20Number:100012&i=5d422f510fbc3b6016f6939a",
        "Cr/IRES_cre//Gt(ROSA)26Sor_CAG/LSL_ZsGreen1": "http://www.hbp.FIXME.org/",
        "Del(5Gtf2i-Fkbp6)1Vcam": "https://dknet.org/data/record/nlx_154697-1/MGI:5662390/resolver?q=Del%285Gtf2i-Fkbp6%291Vcam&l=Del%285Gtf2i-Fkbp6%291Vcam&i=5d4233580fbc3b6016f8c3f2",
        "Del(5Gtf2i-Fkbp6)1Vcam/Vcam": "https://dknet.org/data/record/nlx_154697-1/MGI:5662390/resolver?q=Del%285Gtf2i-Fkbp6%291Vcam&l=Del%285Gtf2i-Fkbp6%291Vcam&i=5d4233580fbc3b6016f8c3f2",
        "lister hooded": "https://dknet.org/data/record/nlx_154697-1/RGD_2312466/resolver?q=lister%20hooded&l=lister%20hooded&i=5d422c300fbc3b6016f4d849",
        "Sprague-Dawley": "https://dknet.org/data/record/nlx_154697-1/MGI:5651135/resolver?q=Sprague-Dawley&l=Sprague-Dawley&i=5d422b8e0fbc3b6016f4825a",
        "SWR": "https://dknet.org/data/record/nlx_154697-1/MGI:2159803/resolver?q=SWR&l=SWR&i=5d422e420fbc3b6016f5fcaa",
        "Tg2576": "https://dknet.org/data/record/nlx_154697-1/MGI:3029285/resolver?q=Tg%28APPSWE%292576Kha&l=Tg%28APPSWE%292576Kha&i=5d4235df0fbc3b6016fa16fb",
        #"Wistar":  "https://rgd.mcw.edu/rgdweb/report/strain/main.html?id=13508588",
        "Wistar": "https://dknet.org/data/record/nlx_154697-1/RGD_12879431/resolver?q=%22Wistar%20Rat%22&l=%22Wistar%20Rat%22&i=5d4228f20fbc3b6016f318fa",
        "BAC_cck/dsred onFVB/ANT": "http://www.hbp.FIXME.org/"
    }
# use RRIDs

class Genotype(OntologyTerm):
    """
    Transgenic modification of the strain.
    """
    iri_map = {
        "BAC_cck/dsred":"http://www.hbp.FIXME.org/",
        "BAC_cck/dsred//BAC_pva/gfp (TgTg)":"http://www.hbp.FIXME.org/",
        "BAC_PV/eGFP": "http://www.hbp.FIXME.org/",
        "BAC_pva/gfp (2)": "http://www.hbp.FIXME.org/",
        "Cre/tdTomato": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:007909/resolver?q=%2A&l=%2A&filter[]=Catalog%20Number:007909&i=5d422e850fbc3b6016f6225c",
        "Cr/IRES_cre//Gt(ROSA)26Sor_CAG/LSL_ZsGreen1": "http://www.hbp.FIXME.org/",
        "C57BL/6J-Tg(Thy1-GCaMP6f)GP5.17Dkim/J": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:025393/resolver?q=%2A&l=&filter[]=Catalog%20Number:025393&i=5d4228390fbc3b6016f2b6a3",
	    "Fmr1KO": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:003025/resolver?q=%2A&l=&filter[]=Catalog%20Number:003025&i=5d422b9b0fbc3b6016f48946",
        "GlyT2-GFP":"http://www.informatics.jax.org/allele/MGI:3835459",
        "IB2-KO": "http://www.hbp.FIXME.org/hbp_brain_region_ontology/1234567",
        "Nlgn3KO/Y; hemizygous": "http://www.informatics.jax.org/allele/MGI:5439278",
        "NL3R451C/Y; hemizygous": "http://www.informatics.jax.org/allele/MGI:3758949",
        "Tg(Thy1-GCaMP6f)GP5.17Dkim/J": "https://dknet.org/data/record/nlx_154697-1/IMSR_JAX:025393/resolver?q=%2A&l=&filter[]=Catalog%20Number:025393&i=5d4228390fbc3b6016f2b6a3",
        "wild type": "https://dknet.org/data/record/nlx_154697-1/MGI:5649737/resolver?q=wild%20type&l=wild%20type&i=5d4223a00fbc3b6016f04b3f",
        "6J-Tg(Thy1-GCaMP6f)GP5.17Dkim/J": "http://www.hbp.FIXME.org/"
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
        "left":"http://uri.interlex.org/ilx_0106154",
        "right":"http://uri.interlex.org/ilx_0110142"
    }

class ChannelType(OntologyTerm):
    """
    The recording method used.
    """
    iri_map = {
        "ECoG": "http://purl.obolibrary.org/obo/NCIT_C116664",
        "ECG": "http://purl.obolibrary.org/obo/NCIT_C38054",
        "EEG": "http://purl.obolibrary.org/obo/NCIT_C38054",
        "EMG": "http://purl.obolibrary.org/obo/NCIT_C38056",
        "ERP": "http://purl.bioontology.org/ontology/SNOMEDCT/251630008",
        "MEG": "http://purl.obolibrary.org/obo/NCIT_C16811",
        "SEEG": "https://en.wikipedia.org/wiki/Stereoelectroencephalography"
    }

class BrainRegion(OntologyTerm):
    """
    A sub-structure or region with the brain.
    """
    iri_map = {
        "anterolateral visual area": "http://uri.interlex.org/ilx_0735646",
        "anteromedial visual area": "http://uri.interlex.org/ilx_0733890",
        "barrel cortex": "http://uri.interlex.org/ilx_0101097",
        "basal ganglia": "http://uri.interlex.org/ilx_0101102",
        "brainstem": "http://uri.interlex.org/ilx_0101444",
        "CA3 field of hippocampus": "http://uri.interlex.org/ilx_0101534",
        "cerebellum": "http://uri.interlex.org/ilx_0101963",
        "cerebral cortex": "http://uri.interlex.org/ilx_0101978",
        "cortex": "http://uri.interlex.org/ilx_0727230",
        "dorsal cortex": "http://uri.interlex.org/ilx_0103432",
        "dorsal striatum": "http://uri.interlex.org/ilx_0103481",
        "frontal association cortex": "http://uri.interlex.org/ilx_0109209",
        "hippocampus": "http://uri.interlex.org/ilx_0105021",  # Ammon's horn
        "hippocampus CA1": "http://purl.obolibrary.org/obo/UBERON_0003881",
        "hippocampus CA3": "http://uri.interlex.org/ilx_0101534",
        "hippocampal formation": "http://uri.interlex.org/ilx_0105009",
        "lobule 5 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004079",
        "lobule 6 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004080",
        "lobule 7 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004081",
        "lobule 8 of the cerebellar vermis": "http://purl.obolibrary.org/obo/UBERON_0004082",
        "motor cortex": "http://uri.interlex.org/ilx_0107119",
        "parietal association area": "http://uri.interlex.org/ilx_0103503",
        "perirhinal cortex": "http://uri.interlex.org/ilx_0108747",
        "posteromedial visual area": "http://uri.interlex.org/ilx_0734159",
        "prefrontal cortex": "http://uri.interlex.org/ilx_0109209",
        "prelimbic cortex": "http://uri.interlex.org/ilx_0106685",
        "primary auditory cortex": "http://uri.interlex.org/ilx_0443027",
        "primary motor cortex": "http://uri.interlex.org/ilx_0109278",
        "primary somatosensory cortex": "http://uri.interlex.org/ilx_0109333",
        "primary visual cortex": "http://uri.interlex.org/ilx_0112514",
        "retina": "http://uri.interlex.org/ilx_0109993",
        "retrosplenial cortex": "http://uri.interlex.org/ilx_0728007",
        "secondary motor cortex": "http://uri.interlex.org/ilx_0109222",
        "secondary visual cortex": "http://uri.interlex.org/ilx_0727119",
        "somatosensory cortex": "http://uri.interlex.org/ilx_0110752",
        "spinal cord": "http://uri.interlex.org/ilx_0110909",
        "stratum pyramidale": "http://uri.interlex.org/ilx_0111081",
        "striatum": "http://uri.interlex.org/ilx_0111098",
        "thalamocortical": "http://uri.interlex.org/ilx_0738230",
        "thalamus": "http://uri.interlex.org/ilx_0111657",
        "ventral hippocampus": "http://uri.interlex.org/ilx_0105021",   # how to distinguish this? Question for Tier 2 folks?
        "visual cortex": "http://uri.interlex.org/ilx_0112513",
        "whole brain": "http://uri.interlex.org/ilx_0101431",
        "5th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004079",
        "6th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004080",
        "7th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004081",
        "8th cerebellar lobule": "http://purl.obolibrary.org/obo/UBERON_0004082"
    }


class CellType(OntologyTerm):
    """A type of neuron or glial cell."""
    iri_map = {
        "cerebellar granule cell": "http://uri.interlex.org/ilx_0101967",
        "cholinergic interneuron": "http://uri.interlex.org/base/ilx_0490357",
        "fast spiking interneuron": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345670",
        "Golgi cell": "http://uri.interlex.org/ilx_0101966",
        "granule cell": "http://uri.interlex.org/ilx_0101967",
        "hippocampus CA1 basket cell": "http://uri.interlex.org/ilx_0105022",
        "hippocampus CA1 bistratified cell": "unknown",
        "hippocampus CA1 ivy neuron": "http://uri.neuinfo.org/nif/nifstd/nlx_35220",
        "hippocampus CA1 lacunosum moleculare neuron": "http://uri.interlex.org/ilx_0105027",
        "hippocampus CA1 pyramidal cell": "http://uri.neuinfo.org/nif/nifstd/sao830368389",
        "hippocampus CA3 pyramidal cell": "http://uri.interlex.org/ilx_0105046",
        "interneuron": "http://uri.interlex.org/ilx_0105593",
        "medium spiny neuron": "http://purl.obolibrary.org/obo/CL_1001474",
        "medium spiny neuron (D1 type)": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345672",
        "medium spiny neuron (D2 type)": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345671",
        "not applicable": "http://www.hbp.FIXME.org/hbp_celltype_ontology/12345673",
        "Purkinje cell": "http://uri.interlex.org/ilx_0101974",
        "pyramidal cell": "http://uri.interlex.org/ilx_0107385",
        "spiny stellate neuron": "http://uri.interlex.org/ilx_0107391",
        "striatal neuron": "http://uri.interlex.org/base/ilx_0111098",
        "L1 neurogliaform cell": "http://uri.interlex.org/base/ilx_0383196",
        "L2 inverted pyramidal cell": "http://uri.interlex.org/ilx_0102369",
        "L2/3 chandelier cell": "http://uri.interlex.org/ilx_0107356",
        "L2/3 pyramidal cell": "http://uri.neuinfo.org/nif/nifstd/nifext_49",
        "L4 Martinotti cell": "http://uri.interlex.org/ilx_0107375",
        "L5 pyramidal cell": "http://uri.interlex.org/ilx_0107385",
        "L5 tufted pyramidal cell": "http://uri.interlex.org/ilx_0107376",
        "L6 inverted pyramidal cell": "http://uri.interlex.org/ilx_0102369"
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
    def initialize(cls, local_file=None):
        if local_file:
            with open(local_file) as fp:
                license_data = json.load(fp)
        else:
            logger.info("Retrieving list of licences")
            spdx_url = "https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json"
            response = requests.get(spdx_url)
            if response.status_code != 200:
                raise Exception("Unable to retrieve license list")
            license_data = response.json()
        for entry in license_data["licenses"]:
            if len(entry["seeAlso"]) > 0:
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
        "c": "https://en.wiktionary.org/wiki/megaohm",
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
    type = "nsg:QuantitativeValue"
    unit_codes = unit_codes

    def __init__(self, value, unit_text, unit_code=None):
        if not isinstance(value, (int, float)):
            raise ValueError("Must be a number")
        self.value = value
        self.unit_text = unit_text
        self.unit_code = unit_code or self.unit_codes[unit_text]

    def __repr__(self):
        return (f'{self.__class__.__name__}({self.value!r} {self.unit_text!r})')

    def __eq__(self, other):
        return (self.value == other.value
                and self.unit_text == other.unit_text
                and self.unit_code == other.unit_code)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_jsonld(self, client=None):
        return {
            "@type": "nsg:QuantitativeValue",
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
    type = "nsg:QuantitativeValueRange"
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
        return (f'{self.__class__.__name__}({self.min!r}-{self.max!r} {self.unit_text!r})')

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
        Field("value", str, "value", required=True),
        Field("period", str, "period", required=True, multiple=True)
    )

    def __init__(self, value, period):
        self.value = value
        if period not in Age.allowed_periods:
            raise ValueError(f"period must be one of {allowed_periods}")
        self.period = period

    def __repr__(self):
        return (f'{self.__class__.__name__}({self.value!r}, {self.period!r})')

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
