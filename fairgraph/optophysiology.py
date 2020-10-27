"""
Metadata for electrophysiology experiments.

The following methods are currently supported:
    - patch clamp recording in brain slices
    - sharp electrode intracellular recording in brain slices

Coming soon:
    - patch clamp recordings in cultured neurons
    - extracellular electrode recording, including tetrodes and multi-electrode arrays

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


import sys
import inspect
try:
    basestring
except NameError:
    basestring = str
from datetime import datetime

from .base import KGObject, KGProxy, KGQuery, cache, lookup, build_kg_object, Field, Distribution
from .commons import QuantitativeValue, BrainRegion, Origin, CellType, StimulusType, License, Shape
from .core import Subject, Person, Protocol
from .minds import Dataset
from .utility import compact_uri, standard_context, as_list

DEFAULT_NAMESPACE = "neuralactivity"

class Position(KGObject):
    """Location within a coordinate system."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/position/v0.1.0"
    type = ["nsg:Position", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
    	"origin": "nsg:origin",
        "x": "nsg:x",
        "ycoordinate": "nsg:y"
        }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("origin", basestring, "origin", required=True),
        Field("xcoordinate", float, "x"),
        Field("ycoordinate", float, "y")
        )

    def __init__(self, name, origin, xcoordinate=None, ycoordinate=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class FluorescenceTrace(KGObject):
    """A time series representing the ΔF/F signal within a region of interest"""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/fluorescencetrace/v0.1.0"
    type = ["nsg:FluorescenceTrace", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "timeStep": "nsg:timeStep",
        "value": "schema:value",
        "description": "schema:description",
        "fluorescenceLabeling": "nsg: fluorescenceLabeling",
        "distribution": {
            "@id": "schema:distribution",
            "@type": "@id"},
        "downloadURL": {
            "@id": "schema:downloadURL",
            "@type": "@id"},
        "mediaType": {
            "@id": "schema:mediaType"
        }
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("time_step", QuantitativeValue, "timeStep", required=True),
        Field("fluorescence_labeling", basestring, "fluorescenceLabeling"),
        Field("time_series", "TimeSeriesExtraction", "^prov:generated", reverse="fluorescence_trace"),
        Field("description", basestring, "description"),
        Field("distribution", Distribution, "distribution")
    )

    def __init__(self, name, time_step, fluorescence_labeling, time_series=None, description=None, distribution=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class TimeSeriesExtraction(KGObject):
    """Process of transforming the series of fluorescence responses within a Region of Interest into a ΔF/F signal"""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/timeseriesextraction/v0.1.0"
    type = ["nsg:TimeSeriesExtraction", "prov:Activity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "value": "schema:value",
        "used": "prov:used",
        "generated": "prov:generated",
	    "hadProtocol":"p  rov:hadProtocol",
        "wasAssociatedWith": "prov:wasAssociatedWith",
    	"citation":"nsg:citation",
    	"code":"nsg:code",
    	"license":"nsg:license"
        }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("fluorescence_trace", FluorescenceTrace, "generated", required=True),
        Field("region_of_interest", "optophysiology.RegionOfInterest", "used"),
        Field("protocol", Protocol, "hadProtocol"),
        Field("people", Person, "wasAssociatedWith", multiple=True),
    	Field("citation", basestring, "citation"),
    	Field("code", basestring, "code"),
    	Field("license", License, "license")
    )

    def __init__(self, name, fluorescence_trace, region_of_interest=None, protocol=None, people=None, citation=None, code=None, license=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class ImageSequence(KGObject):
    """A sequence of images in the same imaging plane, produced by scanning optical microscopy."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/imagesequence/v0.1.0"
    type = ["nsg:ImageSequence", "prov:Entity"]
    context = {
            "schema": "http://schema.org/",
            "prov": "http://www.w3.org/ns/prov#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "name": "schema:name",
            "frameRate": "nsg:frameRate",
            "imageCount": "nsg:imageCount",
            "imageSize": "nsg:imageSize",
            "brainLocation": "nsg:brainLocation",
            "value": "schema:value",
            "extent": "nsg:extent",
            "description": "schema:description",
            "wasGeneratedBy": "prov:wasGeneratedBy",
            "distribution": {
                "@id": "schema:distribution",
                "@type": "@id"},
            "downloadURL": {
                "@id": "schema:downloadURL",
                "@type": "@id"},
            "mediaType": {
                "@id": "schema:mediaType"
            },
            "minds": "https://schema.hbp.eu/"
            }

    fields = (
        Field("name", basestring, "name", required=True),
        Field("frame_rate", QuantitativeValue, "FrameRate", required=True),
        Field("generated_by", "TwoPhotonImaging", "^prov:generated", reverse="image_sequence"),
        Field("image_count", int, "imageCount", required=False),
        Field("image_size", int, "imageSize", required=False), # assumed square
        Field("extent", QuantitativeValue, "extent"),
        Field("brain_location", BrainRegion, "brainRegion", required=False, multiple=True),
        Field("correction_activity", "optophysiology.MotionCorrection", "^prov:used", reverse=["before","after"]),
        Field("distribution", Distribution, "distribution", required=False),
        Field("description", basestring, "description", required=False)
    )

    def __init__(self, name, frame_rate, generated_by=None, image_count=None, image_size=None,
    extent=None, brain_location=None, correction_activity=None, distribution=None, description=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)

class RegionOfInterest(KGObject):
    """A region of interest within an image sequence."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/regionofinterest/v0.9.0"
    type = ["nsg:RegionOfInterest", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "position":"nsg:position",
        "shape": "nsg:geometry",
    	"description":"nsg:description",
    	"classification":"nsg:classification"
        }

    fields = (
        Field("name", basestring, "name", required=True),
        Field("position", Position, "position"),
        Field("shape", basestring, "shape"),
    	Field("classification", basestring, "classification"),
    	Field("description", basestring, "description"),
        Field("selection", "optophysiology.ROISelection","^prov:generated", reverse="regions"),
        Field("time_series", TimeSeriesExtraction,"^prov:used", reverse="region_of_interest"),
    )

    def __init__(self, name, position= None, shape=None, classification=None,
    description=None, selection=None, time_series=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class ROISelection(KGObject):
    """Process of selecting regions of interest, may be manual, semi-automated, or fully automated."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/roiselection/v0.2.0"
    type = ["nsg:ROISelection", "prov:Activity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "used": "prov:used",
        "generated": "prov:generated",
	    "hadProtocol":"p  rov:hadProtocol",
        "wasAssociatedWith": "prov:wasAssociatedWith",
    	"citation":"nsg:citation",
    	"code":"nsg:code",
    	"license":"nsg:license"
        }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("image_sequence", ImageSequence, "used", required=True),
        Field("regions", RegionOfInterest, "generated", required=True),
        Field("protocol", Protocol, "hadProtocol"),
        Field("people", Person, "wasAssociatedWith", multiple=True),
    	Field("citation", basestring, "citation"),
    	Field("code", basestring, "code"),
    	Field("license", License, "license")
    )

    def __init__(self, name, image_sequence, regions, protocol=None, people=None, citation=None, code=None, license=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class CranialWindow(KGObject):
    """A window (partially) through the skull."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/cranialwindow/v0.1.1"
    type = ["nsg:CranialWindow", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "value": "schema:value",
        "name": "schema:name",
        "brainLocation": "nsg:brainLocation",
        "brainRegion": "nsg:brainRegion",
    	"windowType":"nsg:windowType",
    	"diameter":"nsg:diameter",
    	"fluorescenceLabeling":"nsg:fluorescenceLabeling",
        "description": "schema:description",
        "minds": "https://schema.hbp.eu/"
        }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("brain_location", BrainRegion, "brainRegion", multiple=True),
        Field("window_type", basestring, "windowType"),
        Field("diameter", QuantitativeValue, "diameter"),
        Field("fluorescence_labeling", basestring, "fluorescenceLabeling"),
        Field("description", basestring, "description"),
        Field("generated_by", "Craniotomy", "^prov:generated", reverse="cranial_window"),
        Field("activity", ("optophysiology.TwoPhotonImaging", "electrophysiology.ElectrodeImplantationActivity", "electrophysiology.PatchClampActivity"), "^prov:used", reverse=["target", "cranial_window", "recorded_tissue"])
    )

    def __init__(self, name, brain_location=None, window_type=None, diameter=None, fluorescence_labeling=None,
    description=None, generated_by=None, activity=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class Craniotomy(KGObject):
    """Surgical procedure to give optical access through the skull to the brain (dura)."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/craniotomy/v0.2.0"
    type = ["nsg:Craniotomy", "prov:Activity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "generated": "prov:generated",
        "used": "prov:used",
        "anesthesia": "nsg:anesthesia",
        "startedAtTime": "prov:startedAtTime",
        "endedAtTime": "prov:endedAtTime",
        "hadProtocol": "prov:hadProtocol",
        "wasAssociatedWith": "prov:wasAssociatedWith"
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("subject", Subject, "used", required=True),
        Field("cranial_window", CranialWindow, "generated", required=True),
        Field("anesthesia", basestring, "anesthesia"),
	    Field("protocol", Protocol, "hadProtocol"),
        Field("start_time", datetime, "startedAtTime"),
        Field("end_time", datetime, "endedAtTime"),
        Field("people", Person, "wasAssociatedWith", multiple=True)
    )

    def __init__(self, name, subject, cranial_window, anesthesia=None, protocol=None, start_time=None, end_time=None, people=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class Slice(KGObject):  # should move to "core" module?
    """A brain slice."""
    namespace = DEFAULT_NAMESPACE
    _path = "/core/slice/v0.1.0"
    type = ["nsg:Slice", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "name": "schema:name",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "providerId": "nsg:providerId",
        "wasDerivedFrom": "prov:wasDerivedFrom"
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("subject", Subject, "wasDerivedFrom", required=True),
        Field("provider_id", basestring, "providerId"),
        Field("brain_slicing_activity", "BrainSlicingActivity", "^prov:generated", reverse="slices"),
        Field("activity", ("electrophysiology.PatchClampActivity", "optophysiology.TwoPhotonImaging"), "^prov:used", reverse=["recorded_tissue","target"])
    )


class TwoPhotonImaging(KGObject):
    """Two-photon-excited fluorescence laser-scanning microscopy."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/twophotonimaging/v0.1.0"
    #type = ["prov:ExperimentalActivity", "nsg:TwoPhotonImaging"]
    type = ["nsg:TwoPhotonImaging", "prov:Activity"]
    context = {
            "schema": "http://schema.org/",
            "prov": "http://www.w3.org/ns/prov#",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "name": "schema:name",
            "brainLocation": "nsg:brainLocation",
            "value": "schema:value",
            "description": "schema:description",
            "wasGeneratedBy": "prov:wasGeneratedBy",
            "distribution": {
                "@id": "schema:distribution",
                "@type": "@id"},
            "downloadURL": {
                "@id": "schema:downloadURL",
                "@type": "@id"},
            "mediaType": {
                "@id": "schema:mediaType"
            },
            "minds": "https://schema.hbp.eu/",
            "generated": "prov:generated",
            "used": "prov:used",
            "startedAtTime": "prov:startedAtTime",
            "endedAtTime": "prov:endedAtTime",
            "hadProtocol": "prov:hadProtocol",
            "wasAssociatedWith": "prov:wasAssociatedWith",
            "microscope": "nsg:microscope",
            "brainState": "nsg:brainState",
            "anesthesia": "nsg:anesthesia",
            "imagingDepth": "nsg:imagingDepth",
            "laser": "nsg:laser",
            "laserPower": "nsg:laserPower",
            "excitationWavelength": "nsg:excitationWavelength",
            "collectionWavelength": "nsg:collectionWavelength"
            }

    fields = (
        Field("name", basestring, "name", required=True),
        Field("image_sequence", ImageSequence, "generated", required=True),
        Field("target", (Slice, CranialWindow), "used"),
        Field("microscope", basestring, "microscope"),
        Field("brain_state", basestring, "brainState"),
        Field("anesthesia", basestring, "anesthesia"),
        Field("laser", basestring, "laser"),
        Field("excitation_wavelength", QuantitativeValue, "excitationWavelength"),
        Field("power_at_objective", QuantitativeValue, "laserPower"),
        Field("collection_wavelength", QuantitativeValue, "collectionWavelength"),
        Field("imaging_depth", QuantitativeValue, "imagingDepth"),
        Field("distribution", Distribution, "distribution"),
        Field("start_time", datetime, "startedAtTime"),
        Field("end_time", datetime, "endedAtTime"),
	    Field("protocol", Protocol, "hadProtocol"),
        Field("people", Person, "wasAssociatedWith", multiple=True)
    )

    def __init__(self, name, image_sequence=None, target=None, microscope=None, brain_state=None, anesthesia=None, laser=None, excitation_wavelength=None, power_at_objective=None, collection_wavelength=None, imaging_depth=None, distribution=None, start_time=None, end_time=None, protocol=None, people=None, citation=None, code=None, license=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)



class MotionCorrection(KGObject):
    """Correction for x-y movement in image frames."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/motioncorrection/v0.2.0"
    type = ["nsg:MotionCorrection", "prov:Activity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "name": "schema:name",
        "generated": "prov:generated",
        "used": "prov:used",
        "hadProtocol": "prov:hadProtocol",
        "wasAssociatedWith": "prov:wasAssociatedWith",
    	"citation":"nsg:citation",
    	"code":"nsg:code",
    	"license":"nsg:license"
        }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("before", ImageSequence, "used", required=True),
        Field("after", ImageSequence, "generated", required=True),
        Field("protocol", Protocol, "hadprotocol"),
        Field("people", Person, "wasAssociatedWith", multiple=True),
    	Field("citation", basestring, "citation"),
    	Field("code", basestring, "code"),
    	Field("license", License, "license")
    )

    def __init__(self, name, before, after, protocol=None, people=None, citation=None, code=None, license=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class VisualStimulus(KGObject):
    """A generic visual stimulus."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/visualstimulus/v0.1.0"
    type = ["nsg:VisualStimulus", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "minds": "https://schema.hbp.eu/",
        "value": "schema:value",
        "name": "schema:name",
        "description": "schema:description",
        "distribution": {
            "@id": "schema:distribution",
            "@type": "@id"},
        "downloadURL": {
            "@id": "schema:downloadURL",
            "@type": "@id"},
        "mediaType": {
            "@id": "schema:mediaType"
        }
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("description", basestring, "description"),
        Field("distribution", Distribution, "distribution"),
        Field("stimulation", "optophysiology.VisualStimulation", "^prov:used", reverse="stimulus")
    )

    def __init__(self, name, description=None, distribution=None, stimulation=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class VisualStimulation(KGObject):
    """Presentation of a visual stimulus to the subject of the experiment."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/visualstimulation/v0.1.0"
    type = ["nsg:VisualStimulation", "prov:Activity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "used": "prov:used",
        "name": "schema:name",
        "interstimulusInterval": "nsg:interstimulusInterval",
        "refreshRate": "nsg:refreshRate",
        "backgroundLuminance": "nsg:backgroundLuminance",
	    "hadProtocol":"prov:hadProtocol",
        "value": "schema:value",
    	"citation":"nsg:citation",
    	"code":"nsg:code",
    	"license":"nsg:license"
        }

    fields = (
        Field("name", basestring, "name", required=True),
        Field("stimulus", VisualStimulus, "used", required=True),
        Field("interstimulus_interval", QuantitativeValue, "interstimulusInterval"),
        Field("refresh_rate", QuantitativeValue, "refreshRate"),
        Field("background_luminance", QuantitativeValue, "backgroundLuminance"),
        Field("protocol", Protocol, "hadProtocol"),
    	Field("citation", basestring, "citation"),
    	Field("code", basestring, "code"),
    	Field("license", License, "license")
    )

    def __init__(self, name, stimulus, interstimulus_interval=None, refresh_rate=None, background_luminance=None, citation=None, protocol=None, code=None, license=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class ElectrophysiologicalStimulus(KGObject):
    """A generic electrophysiological stimulus."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/electrophysiologicalstimulus/v0.1.0"
    type = ["nsg:ElectrophysiologicalStimulus", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "minds": "https://schema.hbp.eu/",
        "name": "schema:name",
        "description": "schema:description",
        "distribution": {
            "@id": "schema:distribution",
            "@type": "@id"},
        "downloadURL": {
            "@id": "schema:downloadURL",
            "@type": "@id"},
        "mediaType": {
            "@id": "schema:mediaType"
        }
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("description", basestring, "description", required=True),
        Field("distribution", Distribution, "distribution"),
        Field("stimulation", "optophysiology.ElectrophysiologicalStimulation", "^prov:used", reverse="stimulus")
    )

    def __init__(self, name, description, distribution=None, stimulation=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class ElectrophysiologicalStimulation(KGObject):
    """Use of an electrophysiological stimulus in the experiment."""
    namespace = DEFAULT_NAMESPACE
    _path = "/optophysiology/electrophysiologicalstimulation/v0.1.0"
    type = ["nsg:ElectrophysiologicalStimulation", "prov:Activity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "used": "prov:used",
        "name": "schema:name",
	    "hadProtocol": "prov:hadProtocol",
        "value": "schema:value",
    	"citation": "nsg:citation",
    	"code": "nsg:code",
    	"stimulusType": "nsg:stimulusType",
    	"license": "nsg:license"
        }

    fields = (
        Field("name", basestring, "name", required=True),
        Field("electrophysiological_stimulus", ElectrophysiologicalStimulus, "used", required=True),
        Field("stimulus_type", StimulusType, "stimulusType"),
        Field("protocol", Protocol, "hadProtocol"),
    	Field("citation", basestring, "citation"),
    	Field("code", basestring, "code"),
    	Field("license", License, "license")
    )

    def __init__(self, name, electrophysiological_stimulus, stimulus_type=None, citation=None, protocol=None, code=None, license=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)
