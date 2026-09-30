import argparse
from collections import defaultdict
from glob import glob
from itertools import chain
import json
import re
import os
import shutil
import subprocess
import sys

from jinja2 import Environment, select_autoescape, FileSystemLoader

global_aliases = {
    "short_name": "alias",
    "full_name": "name",
    "has_versions": "versions",
    "has_entity": "entities",
    "hashes": "hash",
    "scope": "model_scope",
    "environment_variable": "environment_variables",
}


# The order, most preferred first, in which a generated class picks its single sort key.
# The names are the camelCase schema names used as ``QueryProperty.name`` (e.g. the Python
# attribute ``lookup_label`` is the schema name ``lookupLabel``). ``name`` is preferred because
# its values are human-readable and sort meaningfully; ``lookupLabel`` is put first only for the
# classes listed in SORT_PRIORITY_EXCEPTIONS, where it keeps terms from the same atlas/scheme
# together. ``synonyms`` is excluded: it is list-valued and not a sensible sort key.
# The Knowledge Graph API allows ``"sort": true`` on only one property, at the root level, so
# exactly one property is chosen and it is always a top-level property.
DEFAULT_SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")

# Per-class overrides, most preferred sort property first. The rest of the priority order is
# left unchanged (the full list is emitted into the generated class).
SORT_PRIORITY_EXCEPTIONS = {
    "ParcellationEntity": ("lookupLabel", "name", "fullName", "shortName", "familyName", "abbreviation"),
    "ParcellationEntityVersion": ("lookupLabel", "name", "fullName", "shortName", "familyName", "abbreviation"),
}


reverse_name_map = {
    "RRID": "identifies",
    "about": {
        "LearningResource": "learningResources",
        "Comment": "comments",
        "LivePaperVersion": "publication",
    },
    "abstractionLevel": "isAbstractionLevelOf",
    "accessibility": "isAccessibilityOf",
    "addExistingTerminology": "suggestedIn",
    "ageCategory": "isAgeCategoryOf",
    "anatomicalAxesOrientation": "isOrientationOf",
    "anatomicalLocation": "isLocationOf",
    "anatomicalLocationOfArray": "isLocationOf",
    "anatomicalLocationOfElectrodes": "isLocationOf",
    "anatomicalTarget": "isTargetOf",
    "applicationCategory": "appliesTo",
    "associatedAccount": "belongsTo",
    "associatedProtocol": "usedIn",
    "attribute": "isAttributeOf",
    "author": "authored",
    "authoringParty": "authored",
    "backgroundStrain": "isBackgroundStrainOf",
    "behavioralProtocol": "usedIn",
    "biologicalSex": "isBiologicalSexOf",
    "breedingType": "isBreedingTypeOf",
    "channel": "isChannelOf",
    "chemicalProduct": "usedInAmount",
    "citedPublication": "citedIn",
    "commenter": "comments",
    "communicationProtocol": "usedIn",
    "components": "isComponentOf",  # or "is_part_of" (TODO "components" redundant with "hasComponent"?)
    "conductorMaterial": "isConductorOf",
    "configuration": "isConfigurationOf",
    "constructionType": "usedFor",
    "contactInformation": "isContactInformationOf",
    "contentType": "isDefinedBy",
    "contentTypePattern": "identifiesContentOf",
    "contribution": "contributedTo",
    "contributor": "contribution",
    "coordinateFramework": "isCoordinateFrameworkOf",
    "coordinateSpace": "isCoordinateSpaceOf",
    "coordinator": "coordinatedProjects",
    "copyOf": "hasCopies",
    "country": "isCountryOf",
    "countryOfFormation": "formedIn",
    "criteria": "basedOnProtocolExecution",
    "criteriaQualityType": "usedByAnnotation",  # or "isCriteriaQualityTypeOf"
    "criteriaType": "usedByAnnotation",
    "cultureMedium": "usedIn",
    "cultureType": "isTypeOf",
    "custodian": "isCustodianOf",
    "dataLocation": "isLocationOf",
    "dataType": "isDataTypeOf",
    "defaultImage": "isDefaultImageFor",
    "definedIn": "defines",  # or "containsDefinitionOf",
    "deliveredBy": "stimulationDevice",
    "dependsOn": "isDependencyOf",
    "deploymentType": "isDeploymentTypeOf",
    "descendedFrom": "hasChildren",  # equivalent to "hasParent" ?
    "describedIn": "describes",
    "developer": "developed",
    "device": {
        "ElectrodeArrayUsage": "usage",
        "RecordingActivity": "usedIn",
        "ElectrodePlacement": "placedBy",
        "CellPatching": "usedIn",
        "Recording": "usedFor",
        "Measurement": "usedFor",
        "TissueSampleSlicing": "usedFor",
        "SlicingDeviceUsage": "usage",
        "PipetteUsage": "usage",
        "ElectrodeUsage": "usage",
        "StaticMRIAcquisition": "usedIn",
        "DynamicMRIAcquisition": "usedIn",
        "MRICoilUsage": "usage",
        "MRIScannerUsage": "usage",
    },
    "deviceType": "isTypeOf",  # TODO: replace with "type"?
    "diffusionEncodingParameters": "usedIn",
    "digitalIdentifier": "identifies",
    "diseaseModel": "isModeledBy",
    "distortionCorrection": "usedIn",
    "documentation": "documents",
    "editor": "edited",
    "educationalLevel": "appliesTo",
    "eligibility": "isEligibilityOf",
    "emitter": "emitted",
    "entryPoint": "isEntryPointOf",
    "environment": "usedFor",  # or "isEnvironmentOf"
    "environmentVariable": "definesEnvironmentOf",
    "ethicsAssessment": "appliesTo",
    "ethicsJurisdiction": "appliesTo",
    "experimentalApproach": "usedIn",
    "failureImpact": "isImpactOf",
    "fatSuppressionTechnique": "usedIn",
    "feature": "characterizes",
    "fieldOfView": "usedIn",
    "fileRepository": "files",
    "form": "isFormOf",
    "format": "isFormatOf",
    "fulfilledBy": "fulfils",
    "fullDocumentation": "fullyDocuments",
    "funder": "funded",
    "funding": "funded",
    "generatedBy": "generationDevice",
    "geneticStrainType": "isGeneticStrainTypeOf",  # or "strain"
    "gradientCorrection": "usedIn",
    "groupedBy": "isUsedToGroup",
    "groupingType": {
        "FileBundle": "isUsedToGroup",
        "FilePathPattern": "isDefinedBy",
    },
    "handedness": "subjectStates",  # or "isHandednessOf"
    "hardware": "usedBy",  # or "isPartOfEnvironment"
    "hasComponent": "isPartOf",
    "hasEntity": "isPartOf",
    "hasParent": "hasChildren",  # equivalent to "descendedFrom"
    "hasPart": "isPartOf",
    "hasVersion": "isVersionOf",
    "holder": "holdsCopyright",  # or "intellectualProperty",
    "hostedBy": "hosts",
    "implements": "isImplementedBy",
    "inRelationTo": "assessment",  # equivalent to "about" ?
    "input": "isInputTo",
    "inputData": "isInputTo",  # could use just "input" ?
    "inputFormat": "isInputFormatOf",
    "inspiredBy": "inspired",
    "insulatorMaterial": "composes",
    "intendedMountingLocation": "isIntendedLocationOf",
    "interface": "isInterfaceOf",
    "interfaceType": "isTypeOf",
    "isAlternativeVersionOf": "isAlternativeVersionOf",  # ??!!
    "isBasedOn": "hasDerived",
    "isNewVersionOf": "isOldVersionOf",
    "isPartOf": "hasParts",  # hasComponent ?
    "isPrecededBy": "precedes",
    "isVariantOf": "hasVariants",
    "isVersionOf": "hasVersions",
    "jurisdiction": "appliesTo",
    "keyword": "describes",
    "labelingCompound": "labels",
    "language": "usedIn",
    "laterality": "isLateralityOf",
    "launchConfiguration": "isLaunchConfigurationOf",
    "license": "isAppliedTo",  # or "governsSharingOf"
    "manufacturer": "manufactured",  # or "product"
    "material": "composes",
    "measuredQuantity": "measurement",
    "measuredWith": "usedToMeasure",
    "member": "isMemberOf",
    "memberOf": "hasMembers",
    "metadataLocation": "describes",
    "minValueUnit": "range",
    "maxValueUnit": "range",
    "modificationProfile": "isProfileOf",
    "molecularEntity": "composes",
    "motionCorrection": "usedIn",
    "mountingLocation": "isMountingLocationOf",
    "mountingType": "isMountingTypeOf",
    "MRIWeighting": "usedIn",
    "MTPulseShape": "usedIn",
    "nativeUnit": "usedBy",
    "obtainedWith": "isUsedToObtain",
    "operatingDevice": "usedBy",
    "operatingSystem": "usedBy",
    "organization": "affiliations",
    "origin": "sample",
    "output": "isOutputOf",  # or "generatedBy"
    "outputData": "isOutputOf",  # replace with "output"?
    "outputFormat": "isOutputFormatOf",
    "owner": "isOwnerOf",  # or "devices"
    "parallelAcquisitionTechnique": "usedIn",
    "pathology": "specimenState",
    "paymentModel": "isPaymentModelOf",
    "performedBy": "activities",
    "person": "affiliations",
    "pipetteSolution": "usedIn",
    "preferredDisplayColor": "preferredBy",
    "preparationDesign": "usedFor",
    "preparationType": "usedIn",
    "previewImage": "isPreviewOf",
    "previousRecording": "nextRecording",
    "previousRegularTimeSeries": "nextRegularTimeSeries",
    "process": "isProcessOf",
    "productSource": "isSourceOf",
    "programmingLanguage": "usedIn",
    "protocol": "usedIn",
    "provider": "isProviderOf",  # or "provided",
    "publicationStatus": "isStatusOf",
    "publisher": "published",
    "qualitativeOverlap": "assessment",
    "recipe": "defined",  # or "defines"
    "recordedWith": "usedToRecord",
    "reference": "isReferenceOf",
    "referenceData": "isReferenceFor",
    "referenceDataAcquisition": "isReferenceFor",
    "registrationData": "usedIn",
    "reinforcementType": "usedFor",
    "relatedInterspeciesAnatomy": "interspeciesRelation",
    "relatedPublication": "relatedTo",
    "relatedUBERONTerm": "defines",
    "relevantFor": "hasProperties",
    "repository": "containsContentOf",
    "scope": "isScopeOf",
    "scoreType": "isScoreTypeOf",
    "serializationFormat": "usedBy",
    "service": {
        "ServiceLink": "linkedFrom",
        "AccountInformation": "hasAccounts",
        "ServiceDeployment": "deployments",
    },
    "setup": "usedIn",
    "signalDirectionality": "usedIn",
    "sliceOrientation": "usedIn",
    "slicingDevice": "usedIn",  # TODO: slicingDevice --> device?
    "slicingPlane": "usedIn",
    "software": "usedIn",
    "source": "isSourceOf",
    "sourceData": "isSourceDataOf",
    "spatialEncoding": "usedIn",
    "specialUsageRole": "file",
    "species": "isSpeciesOf",
    "specification": "specifies",
    "specificationFormat": "isSpecificationFormatOf",
    "specimenOrientation": "usedIn",
    "spoilingTechnique": "usedIn",
    "stage": "isPartOf",
    "startedBy": "started",
    "status": "isStatusOf",
    "stimulation": "usedIn",
    "stimulus": "isStimulusFor",
    "stimulusType": "usedIn",
    "structurePattern": "structures",
    "studiedSpecimen": "hasStudyResultsIn",  # "isPartOfStudy"
    "studiedState": "isStateOf",
    "studyTarget": "studiedIn",
    "targetAnatomy": "isTargetOf",
    "targetIdentificationType": "isTypeOf",
    "technique": "usedIn",
    "template": "isTemplateOf",
    "tissueBathSolution": "usedIn",
    "type": "isTypeOf",
    "typeOfUncertainty": "value",
    "unit": {
        "Channel": "usedIn",
        "QuantitativeValue": "value",
        "QuantitativeValueArray": "value",
    },
    "usageCondition": "appliesTo",
    "usedCoils": "usedIn",
    "usedSpecies": "commonCoordinateSpace",
    "usedSpecimen": "usedIn",
    "usedTaxon": "usedIn",
    "uses": "isUsedBy",
    "variation": "usedIn",
    "vendor": "stocks",
    "wasInformedBy": "informed",
}

number_names = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}


def generate_python_name(json_name):
    python_name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", json_name.strip())
    python_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", python_name).lower()
    replacements = [("-", "_"), (".", "_"), ("+", "plus"), ("#", "sharp"), (",", "comma"), ("(", ""), (")", "")]
    for before, after in replacements:
        python_name = python_name.replace(before, after)
    if python_name[0] in number_names:  # Python variables can't start with a number
        python_name = number_names[python_name[0]] + python_name[1:]
    if not python_name.isidentifier():
        raise NameError(f"Cannot generate a valid Python name from '{json_name}'")
    return python_name


def generate_doc(prop, obj_title):
    if obj_title.upper() == obj_title:  # for acronyms, e.g. DOI
        obj_title_readable = obj_title
    elif "UBERON" in obj_title:
        obj_title_readable = obj_title
    else:
        obj_title_readable = re.sub("([A-Z])", r" \g<0>", obj_title).strip().lower()
    doc = prop.get("description", "no description available")
    doc = doc.replace("someone or something", f"the {obj_title_readable}")
    doc = doc.replace("something or somebody", f"the {obj_title_readable}")
    doc = doc.replace("something or someone", f"the {obj_title_readable}")
    doc = doc.replace("a being or thing", f"the {obj_title_readable}")
    return doc


def invert_dict(D):
    newD = {}
    for key, values in D.items():
        for value in values:
            newD[value] = key
    return newD


DEFAULT_SPACES = {
    "v4": {
        "chemicals": {"default": "in-depth"},
        "core": invert_dict(
            {
                "common": [
                    "Affiliation",
                    "Comment",
                    "Configuration",
                    "Consortium",
                    "Funding",
                    "GRIDID",
                    "HANDLE",
                    "HardwareSystem",
                    "IdentifiersDotOrgID",
                    "ORCID",
                    "Organization",
                    "Person",
                    "Project",
                    "Query",
                    "RORID",
                    "TermSuggestion",
                    "WebResource",
                    "RRID",
                    "AccountInformation",  # or does this go in "restricted"?
                ],
                "files": [
                    "ContentTypePattern",
                    "File",
                    "FileBundle",
                    "FilePathPattern",
                    "FileRepositoryStructure",
                    "Hash",
                ],
                "dataset": [
                    "Contribution",
                    "Copyright",
                    "DOI",
                    "Dataset",
                    "DatasetVersion",
                    "FileArchive",
                    "FileRepository",
                    "ISBN",
                    "ISSN",
                    "NumericalParameter",
                    "ParameterSet",
                    "PropertyValueList",
                    "Protocol",
                    "ExperimentalActivity",
                    "ProtocolExecution",
                    "QuantitativeValue",
                    "QuantitativeValueRange",
                    "QuantitativeValueArray",
                    "ResearchProductGroup",
                    "ServiceLink",
                    "StringParameter",
                    "Subject",
                    "SubjectGroup",
                    "SubjectGroupState",
                    "SubjectState",
                    "TissueSample",
                    "TissueSampleCollection",
                    "TissueSampleCollectionState",
                    "TissueSampleState",
                    "BehavioralProtocol",
                    "Stimulation",
                    "Strain",
                    "Setup",
                ],
                "model": ["Model", "ModelVersion"],
                "software": ["SWHID", "Software", "SoftwareVersion"],
                "restricted": ["ContactInformation"],
                "metadatamodel": ["MetaDataModel", "MetaDataModelVersion"],
                "controlled": ["License", "ContentType"],
                "webservice": ["WebService", "WebServiceVersion"],
            }
        ),
        "computation": {"default": "computation"},
        "controlled_terms": {"default": "controlled"},
        "sands": invert_dict(
            {
                "spatial": [
                    "AnatomicalEntity",
                    "Annotation",
                    "CoordinatePoint",
                    "CustomAnatomicalEntity",
                    "CustomAnnotation",
                    "CustomCoordinateSpace",
                    "Image",
                    "QualitativeRelationAssessment",
                    "QuantitativeRelationAssessment",
                ],
                "atlas": [
                    "AnatomicalTargetPosition",
                    "AtlasAnnotation",
                    "BrainAtlas",
                    "BrainAtlasVersion",
                    "Circle",
                    "ColorMap",
                    "CommonCoordinateSpace",
                    "CommonCoordinateSpaceVersion",
                    "CoordinatePoint",
                    "Ellipse",
                    "ParcellationEntity",
                    "ParcellationTerminology",
                    "ParcellationTerminologyVersion",
                    "ParcellationEntityVersion",
                    "Rectangle",
                    "SingleColor",
                ],
            }
        ),
        "publications": {"default": "livepapers"},
        "ephys": {"default": "in-depth"},
        "specimen_prep": {"default": "in-depth"},
        "stimulation": {"default": "in-depth"},
    },
    "v5": {
        "chemicals": {"default": "in-depth"},
        "core": invert_dict(
            {
                "common": [
                    "Affiliation",
                    "Comment",
                    "Configuration",
                    "Consortium",
                    "Funding",
                    "HANDLE",
                    "HardwareProduct",
                    "IdentifiersDotOrgID",
                    "ISNI",
                    "LEI",
                    "ORCID",
                    "Organization",
                    "Person",
                    "Project",
                    "RORID",
                    "WebResource",
                    "RRID",
                    "AccountInformation",
                    "GenericIdentifier",
                    "Membership",
                    "GeoCoordinates",
                    "Location",
                ],
                "files": [
                    "ContentTypePattern",
                    "File",
                    "FileBundle",
                    "FilePathPattern",
                    "FileRepositoryStructure",
                    "Hash",
                    "LocalFile",
                ],
                "dataset": [
                    "Contribution",
                    "Copyright",
                    "DOI",
                    "Dataset",
                    "DatasetVersion",
                    "FileArchive",
                    "FileRepository",
                    "ISBN",
                    "ISSN",
                    "NumericalProperty",
                    "PropertyValueList",
                    "Protocol",
                    "ProtocolExecution",
                    "QuantitativeValue",
                    "QuantitativeValueRange",
                    "QuantitativeValueArray",
                    "ResearchProductGroup",
                    "ServiceLink",
                    "StringProperty",
                    "Subject",
                    "SubjectGroup",
                    "SubjectGroupState",
                    "SubjectState",
                    "TissueSample",
                    "TissueSampleCollection",
                    "TissueSampleCollectionState",
                    "TissueSampleState",
                    "BehavioralProtocol",
                    "Strain",
                    "Setup",
                    "CustomPropertySet",
                    "StockNumber",
                    "SpecimenAge",
                    "SpecimenWeight",
                    "Accessibility",
                    "Dependency",
                    "UsageAgreement",
                ],
                "model": ["Model", "ModelVersion"],
                "software": ["SWHID", "Software", "SoftwareVersion", "Service"],
                "restricted": ["ContactInformation"],
                "metadatamodel": ["MetaDataModel", "MetaDataModelVersion"],
                "controlled": ["License", "ContentType"],
                "interface": ["Interface", "InterfaceVersion", "DeployedInterface"],
                "in-depth": [
                    "GridImage",
                    "GridImageSequence",
                    "GridImageStack",
                    "GridVolume",
                    "GridVolumeSequence",
                    "Measurement",
                    "RegularTimeSeries",
                ],
            }
        ),
        "computation": {"default": "computation"},
        "controlled_terms": {"default": "controlled"},
        "sands": invert_dict(
            {
                "spatial": [
                    "CoordinatePoint",
                    "CustomAnatomicalEntity",
                    "CustomAnnotation",
                    "CustomCoordinateFramework",
                    "QualitativeRelationAssessment",
                    "QuantitativeRelationAssessment",
                    "ViewerSpecification",
                ],
                "atlas": [
                    "AnatomicalAtlas",
                    "AnatomicalAtlasVersion",
                    "AnatomicalTargetPosition",
                    "AtlasAnnotation",
                    "CentroidalPyramid",
                    "Circle",
                    "CircularSector",
                    "CommonCoordinateFramework",
                    "CommonCoordinateFrameworkVersion",
                    "CoordinatePoint",
                    "Cube",
                    "Ellipse",
                    "Ellipsoid",
                    "EquilateralTriangle",
                    "Frustum",
                    "IsoscelesTriangle",
                    "Kite",
                    "ParcellationEntity",
                    "ParcellationEntityVersion",
                    "ParcellationTerminology",
                    "ParcellationTerminologyVersion",
                    "Parallelogram",
                    "Rectangle",
                    "RegularPolygon",
                    "Rhombus",
                    "RightCone",
                    "RightCylinder",
                    "RightPrism",
                    "RightTriangle",
                    "SingleColor",
                    "Sphere",
                    "Spheroid",
                    "Square",
                    "Trapezoid",
                    "Triangle",
                ],
            }
        ),
        "publications": {"default": "livepapers"},
        "ephys": {"default": "in-depth"},
        "specimen_prep": {"default": "in-depth"},
        "stimulation": {"default": "in-depth"},
        "neuroimaging": {"default": "in-depth"},
    },
}


def get_default_space(schema_group, cls_name, version="v4"):
    spaces = DEFAULT_SPACES[version]
    if schema_group not in spaces:
        raise Exception(f"Please update DEFAULT_SPACES['{version}'] for the {schema_group} module")
    if cls_name in spaces[schema_group]:
        return spaces[schema_group][cls_name]
    else:
        try:
            return spaces[schema_group]["default"]
        except KeyError:
            raise KeyError(f"An entry for '{cls_name}' is missing from DEFAULT_SPACES['{version}']['{schema_group}']")


# in general, we use the required properties when deciding whether a given object already exists
# in the KG. Sometimes this method is inappropriate or undesired, and so for some classes
# we use a custom set of properties.
custom_existence_queries = {
    "LaunchConfiguration": ("executable", "name"),
    "Person": ("given_name", "family_name"),
    "File": ("iri", "hashes"),
    "FileRepository": ("iri",),
    "License": ("alias",),
    "DOI": ("identifier",),
    "GRIDID": ("identifier",),
    "HANDLE": ("identifier",),
    "ISBN": ("identifier",),
    "ORCID": ("identifier",),
    "RORID": ("identifier",),
    "SWHID": ("identifier",),
    "WebResource": ("iri",),
    "Dataset": ("short_name",),
    "DatasetVersion": ("short_name", "version_identifier"),
    "MetaDataModel": ("short_name",),
    "MetaDataModelVersion": ("short_name", "version_identifier"),
    "Model": ("full_name",),  # here we use 'full_name' instead of 'short_name' for backwards compatibility
    "ModelVersion": ("full_name", "version_identifier"),
    "Project": ("short_name",),
    "Software": ("short_name",),
    "SoftwareVersion": ("short_name", "version_identifier"),
    "WebService": ("short_name",),
    "WebServiceVersion": ("short_name", "version_identifier"),
    "Protocol": ("name",),
    "BrainAtlas": ("digital_identifier",),
    "BrainAtlasVersion": ("short_name", "version_identifier"),
    "CommonCoordinateSpace": ("short_name", "version_identifier"),
    "ParcellationEntity": ("name",),
    "ParcellationEntityVersion": ("name", "version_identifier"),
    "ParcellationTerminologyVersion": ("short_name", "version_identifier"),
    "CustomCoordinateSpace": ("name",),
    "WorkflowRecipe": ("full_name",),
    "WorkflowRecipeVersion": ("full_name", "version_identifier"),
    "ValidationTest": ("full_name", "short_name"),
    "ValidationTestVersion": ("short_name", "version_identifier"),
    "LivePaper": ("full_name", "short_name"),
    "LivePaperVersion": ("short_name", "version_identifier"),
    "LivePaperResourceItem": ("name", "iri", "is_part_of"),
    "ScholarlyArticle": ("name",),
    "WorkflowExecution": ("stages",),
    "Configuration": ("configuration",),
    "Periodical": ("abbreviation",),
    "AmountOfChemical": ("chemical_product", "amount"),
    "QuantitativeValue": ("value", "unit", "uncertainties"),
    "Hash": ("algorithm", "digest"),
    # v5 additions
    "AnatomicalAtlas": ("digital_identifier",),
    "AnatomicalAtlasVersion": ("short_name", "version_identifier"),
    "CommonCoordinateFramework": ("short_name", "version_identifier"),
    "CommonCoordinateFrameworkVersion": ("short_name", "version_identifier"),
    "CustomCoordinateFramework": ("name",),
    "GenericIdentifier": ("identifier",),
    "ISNI": ("identifier",),
    "LEI": ("identifier",),
    "Interface": ("short_name",),
    "InterfaceVersion": ("short_name", "version_identifier"),
    "LocalFile": ("name", "hashes"),
    "Service": ("short_name",),
}


def get_existence_query(cls_name, properties):
    if cls_name in custom_existence_queries:
        return custom_existence_queries[cls_name]

    for prop in properties:
        if prop["name"] == "lookup_label":
            return ("lookup_label",)

    required_property_names = []
    for prop in properties:
        if prop["required"]:
            required_property_names.append(prop["name"])
    return tuple(required_property_names)


def property_name_sort_key(property_name):
    """Sort the name prop to be first"""
    priorities = {
        "name": "0",
        "fullName": "0",
        "alias": "1",
        "shortName": "1",
        "lookup_label": "3",
    }
    return priorities.get(property_name, property_name)


def generate_class_name(iri, module_map=None, openminds_version="v4"):
    assert isinstance(iri, str)
    class_name = iri.split("/")[-1]
    module_name = generate_python_name(module_map[iri])
    return f"openminds.{openminds_version}.{module_name}.{class_name}"


def get_controlled_terms_table(type_):
    return ""


preamble_for_download = """from urllib.request import urlretrieve
from pathlib import Path
from fairgraph.utility import accepted_terms_of_use"""

preamble = {
    "File": """import os
import mimetypes
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import quote, urlparse, urlunparse
from .hash import Hash
from .content_type import ContentType
from ..miscellaneous.quantitative_value import QuantitativeValue
from ...controlled_terms.unit_of_measurement import UnitOfMeasurement
from fairgraph.utility import accepted_terms_of_use, sha1sum

mimetypes.init()""",
    "DatasetVersion": preamble_for_download,
    "ModelVersion": preamble_for_download,
    "BrainAtlasVersion": preamble_for_download,
    "CommonCoordinateSpaceVersion": preamble_for_download,
    "CommonCoordinateFrameworkVersion": preamble_for_download,
    "AnatomicalAtlasVersion": preamble_for_download,
    "ScholarlyArticle": """from fairgraph.utility import as_list
from .publication_issue import PublicationIssue
from .periodical import Periodical""",
}


class FairgraphClassBuilder:
    """docstring"""

    def __init__(self, schema_file_path: str, root_path: str, target_path_root: str, openminds_version: str = "v4"):
        self.template_name = "fairgraph_module_template.py.txt"
        self.env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))), autoescape=select_autoescape()
        )
        _relative_path_without_extension = (
            schema_file_path[len(root_path) :].replace(".schema.omi.json", "").split("/")
        )
        self.relative_path_without_extension = [
            generate_python_name(part) for part in _relative_path_without_extension[1:]
        ]
        with open(schema_file_path, "r") as schema_f:
            self._schema_payload = json.load(schema_f)
        self.target_path_root = target_path_root
        self.openminds_version = openminds_version

    def _target_file_without_extension(self) -> str:
        return os.path.join(*self.relative_path_without_extension)

    def translate(self, embedded=None, linked=None, module_map=None):
        openminds_version = self.openminds_version

        def get_type(prop):
            type_map = {
                "string": "str",
                "integer": "int",
                "number": "Real",
                "date": "date",
                "date-time": "datetime",
                "time": "time",
                "iri": "IRI",
                "email": "str",  # todo: add an Email class for validation?
                "ECMA262": "str",  #       ...
            }
            if "_linkedTypes" in prop:
                types = []
                for item in prop["_linkedTypes"]:
                    class_name = item.split("/")[-1]
                    openminds_module = generate_python_name(module_map[item])
                    types.append(f"openminds.{openminds_module}.{class_name}")
                if len(types) == 1:
                    types = f'"{types[0]}"'
                return types
            elif "_embeddedTypes" in prop:
                types = []
                for item in prop["_embeddedTypes"]:
                    class_name = item.split("/")[-1]
                    openminds_module = generate_python_name(module_map[item])
                    types.append(f"openminds.{openminds_module}.{class_name}")
                if len(types) == 1:
                    types = f'"{types[0]}"'
                return types
            elif "type" in prop:
                if isinstance(prop["type"], list):
                    return [type_map[item] for item in prop["type"]]
                else:
                    if prop["type"] == "array":
                        return type_map[prop["items"]["type"]]
                    elif "_formats" in prop:
                        assert isinstance(prop["_formats"], list)
                        if len(prop["_formats"]) > 1:
                            types = f"[{', '.join([type_map[p] for p in prop['_formats']])}]"
                            return types
                        return type_map[prop["_formats"][0]]
                    else:
                        return type_map[prop["type"]]

            else:
                raise NotImplementedError

        class_name = self._schema_payload["name"]
        module_name = self.relative_path_without_extension[0]
        if self._schema_payload["_type"] in embedded:
            base_class = "KGEmbedded"
            default_space = None
            standard_init_properties = ""
        else:
            base_class = "KGObject"
            default_space = get_default_space(module_name, class_name, version=openminds_version)
            standard_init_properties = "id=id, space=space, release_status=release_status, "
        properties = []
        plurals_special_cases = {
            # because this is a single item (PropertyValueList), but that item contains a list
            # temporarily removing this, since plurals are now defined in the openMINDS schemas,
            # we'll need to make a PR to change the plural there.
            # for now, handling this by adding a global alias, see above
            # "environmentVariable": "environmentVariables",
        }
        aliases = {}
        for iri, prop in self._schema_payload["properties"].items():
            allow_multiple = prop.get("type", "") == "array"
            if allow_multiple:
                property_name = prop["namePlural"]
            elif prop["name"] in plurals_special_cases:
                property_name = plurals_special_cases[prop["name"]]
            else:
                property_name = prop["name"]
            python_name = generate_python_name(property_name)
            properties.append(
                {
                    "name": python_name,
                    "type_str": get_type(prop),  # compress using JSON-LD context
                    "iri": f"{prop['name']}",
                    "allow_multiple": allow_multiple,
                    "required": iri in self._schema_payload.get("required", []),
                    "doc": generate_doc(prop, class_name),
                    # "instructions": prop.get("_instruction", "no instructions available"),
                    "formatting": prop.get("formatting", None),
                    "multiline": prop.get("multiline", None),
                    "unique_items": prop.get("uniqueItems", False),
                    "min_items": prop.get("minItems", None),
                    "max_items": prop.get("maxItems", None),
                }
            )
            if python_name in global_aliases:
                aliases[global_aliases[python_name]] = python_name
        reverse_properties = []
        forward_property_names = set(prop["name"] for prop in properties)
        conflict_resolution = {
            "is_part_of": "is_also_part_of",
        }
        if linked:
            linked_from = linked[self._schema_payload["_type"]]
            for reverse_link_name in linked_from:
                unique_forward_iris = set(linked_from[reverse_link_name][0])
                types_str = [
                    generate_class_name(iri, module_map, openminds_version=openminds_version)
                    for iri in linked_from[reverse_link_name][2]
                ]
                if len(unique_forward_iris) == 1:
                    (forward_iri,) = unique_forward_iris
                    forward_link_names = set(linked_from[reverse_link_name][1])
                    if len(forward_link_names) == 1:
                        (forward_link_name,) = forward_link_names
                    else:
                        forward_link_name = sorted(forward_link_names)[0]
                        print(f"Multiple forward link names found: {forward_link_names}, using {forward_link_name}")
                        # todo: we should fix this at some point, using just the first forward_link_name causes things to break
                        #       making this a dictionary keyed by class names should work?
                    _forward_link_name_python = generate_python_name(forward_link_name)
                    iri = forward_iri
                    doc = f"reverse of '{_forward_link_name_python}'"
                    types_str = sorted(types_str)
                    if len(types_str) == 1:
                        types_str = f'"{types_str[0]}"'
                else:
                    backwards_compatible = True
                    if backwards_compatible:
                        forward_iri = sorted(set(linked_from[reverse_link_name][0]))
                        forward_link_name = sorted(set(linked_from[reverse_link_name][1]))
                        types_str = sorted(types_str)
                    else:
                        # this is a better solution, since we keep the match between types and names
                        # in the order of the lists, but is not backwards compatible
                        forward_iri = linked_from[reverse_link_name][0]
                        forward_link_name = linked_from[reverse_link_name][1]
                    _forward_link_name_python = [generate_python_name(name) for name in forward_link_name]
                    iri = [part for part in forward_iri]
                    doc = "reverse of " + ", ".join(name for name in _forward_link_name_python)
                reverse_name_python = generate_python_name(reverse_link_name)
                if reverse_name_python in forward_property_names:
                    if reverse_name_python in conflict_resolution:
                        reverse_name_python = conflict_resolution[reverse_name_python]
                    else:
                        raise Exception(
                            "The following name appears as both a forward and reverse name "
                            f"for {class_name}: {reverse_name_python}"
                        )
                reverse_properties.append(
                    {
                        "name": reverse_name_python,
                        "type_str": types_str,
                        "_forward_name_python": _forward_link_name_python,
                        "iri": iri,
                        "allow_multiple": True,
                        "required": False,
                        "doc": doc,
                    }
                )

        additional_methods = ""
        if os.path.exists(f"additional_methods/{class_name}.py.txt"):
            with open(f"additional_methods/{class_name}.py.txt") as fp:
                additional_methods = fp.read()
        self.context = {
            "openminds_version": openminds_version,
            "docstring": self._schema_payload.get("description", "<description not available>"),
            "base_class": base_class,
            "preamble": preamble.get(class_name, ""),  # default value, may be updated below
            "module_name": module_name,
            "class_name": class_name,
            "default_space": default_space,
            "openminds_type": self._schema_payload["_type"],
            "properties": sorted(properties, key=lambda p: p["name"]),
            "reverse_properties": sorted(reverse_properties, key=lambda p: p["name"]),
            "existence_query_properties": get_existence_query(class_name, properties),
            "standard_init_properties": standard_init_properties,
            "additional_methods": additional_methods,
            "aliases": aliases,
            "sort_priority": SORT_PRIORITY_EXCEPTIONS.get(class_name, DEFAULT_SORT_PRIORITY),
            "constructor_arguments": sorted(
                [p["name"] for p in chain(properties, reverse_properties)] + list(aliases.keys()),
                key=property_name_sort_key,
            ),
        }
        import_map = {
            "date": "from datetime import date",
            "datetime": "from datetime import datetime",
            "time": "from datetime import time",
            "IRI": "from openminds import IRI",
            "[datetime, time]": "from datetime import datetime, time",
            "Real": "from numbers import Real",
        }
        extra_imports = set()
        for prop in self.context["properties"]:
            if isinstance(prop["type_str"], list):
                for t in prop["type_str"]:
                    imp = import_map.get(t, None)
                    if imp:
                        extra_imports.add(imp)
            else:
                imp = import_map.get(prop["type_str"], None)
                if imp:
                    extra_imports.add(imp)
        if extra_imports:
            self.context["preamble"] += "\n" + "\n".join(sorted(extra_imports))
        if module_name == "controlled_terms":
            self.context["docstring"] += get_controlled_terms_table(self._schema_payload["_type"])

    def build(self, embedded=None, linked=None, module_map=None):
        target_file_path = os.path.join(self.target_path_root, f"{self._target_file_without_extension()}.py")
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        self.translate(embedded=embedded, linked=linked, module_map=module_map)

        with open(target_file_path, "w") as target_file:
            contents = self.env.get_template(self.template_name).render(self.context)
            target_file.write(contents)

        return (self._target_file_without_extension().replace("/", "."), self.context["class_name"])

    def get_edges(self):
        embedded = set()
        linked = {}
        for prop in self._schema_payload["properties"].values():
            for emb in prop.get("_embeddedTypes", []):
                embedded.add(emb)
            for lnk in prop.get("_linkedTypes", []):
                reverse_link_name = prop["nameForReverseLink"]
                if reverse_link_name is None:
                    reverse_link_name = reverse_name_map[prop["name"]]
                allow_multiple = prop.get("type", "") == "array"
                linked[lnk] = (
                    self._schema_payload["_type"],
                    prop["name"],  # property name
                    prop["namePlural"] if allow_multiple else prop["name"],  # forward link name
                    reverse_link_name,
                )  # linked from (cls, prop name, prop name plural, reverse name)
                # if self._schema_payload["_type"].endswith("File"):
        return embedded, linked

    def get_module_map(self):
        return self._schema_payload["_type"], self._schema_payload["_module"]


def generate_version(openminds_root, openminds_version, target_path):
    """Generate fairgraph classes for a single openMINDS version."""
    version_target_path = os.path.join(target_path, openminds_version)
    if os.path.exists(version_target_path):
        shutil.rmtree(version_target_path)
    openminds_root = os.path.realpath(openminds_root)

    schema_file_paths = glob(os.path.join(openminds_root, f"**/*.schema.omi.json"), recursive=True)
    python_modules = defaultdict(list)

    # Zeroth pass - map schemas to modules
    module_map = {}
    for schema_file_path in schema_file_paths:
        type_, module_name = FairgraphClassBuilder(
            schema_file_path, openminds_root, version_target_path, openminds_version
        ).get_module_map()
        module_map[type_] = module_name

    # First pass - figure out which schemas are embedded and which are linked
    embedded = set()
    linked = defaultdict(dict)
    for schema_file_path in schema_file_paths:
        embedded_in, linked_from = FairgraphClassBuilder(
            schema_file_path, openminds_root, version_target_path, openminds_version
        ).get_edges()
        embedded.update(embedded_in)
        for openminds_type, (link_type, property_name, forward_name, reverse_name) in linked_from.items():
            if link_type not in embedded:
                if isinstance(reverse_name, dict):
                    cls_name = link_type.split("/")[-1]
                    reverse_name = reverse_name[cls_name]
                if reverse_name in linked[openminds_type]:
                    linked[openminds_type][reverse_name][0].append(property_name)
                    linked[openminds_type][reverse_name][1].append(forward_name)
                    linked[openminds_type][reverse_name][2].append(link_type)
                else:
                    linked[openminds_type][reverse_name] = ([property_name], [forward_name], [link_type])
    conflicts = set(linked).intersection(embedded)
    if conflicts:
        print(f"Found schema(s) that are both linked and embedded: {conflicts}")
        # conflicts should not happen in new versions.
        for schema_identifier in conflicts:
            linked.pop(schema_identifier, None)

    # Second pass - create a Python module for each openMINDS schema
    for schema_file_path in schema_file_paths:
        module_path, class_name = FairgraphClassBuilder(
            schema_file_path, openminds_root, version_target_path, openminds_version
        ).build(embedded=embedded, linked=linked, module_map=module_map)

        parts = module_path.split(".")
        parent_path = ".".join(parts[:-1])
        python_modules[parent_path].append((parts[-1], class_name))

    # Now create additional files, e.g. __init__.py
    openminds_modules = set()
    for path, classes in python_modules.items():
        dir_path = path.split(".")
        openminds_modules.add(dir_path[0])
        # first write __init__ for submodule (or top-level module if no submodules)
        init_file_path = os.path.join(version_target_path, *(dir_path + ["__init__.py"]))
        with open(init_file_path, "w") as fp:
            for class_module, class_name in sorted(classes, key=lambda entry: entry[0]):
                fp.write(f"from .{class_module} import {class_name}\n")

        # now write __init__ for top-level module if submodules
        child_dir = dir_path[-1]
        dir_path = dir_path[:-1]
        if len(dir_path) == 1:
            init_file_path = os.path.join(version_target_path, *(dir_path + ["__init__.py"]))
            with open(init_file_path, "a") as fp:
                class_names = ", ".join(class_name for _, class_name in classes)
                fp.write(f"from .{child_dir} import ({class_names})\n")

    for om_module in openminds_modules:
        with open("init_template.py.txt") as fp:
            om_module_functions = fp.read()
        init_file_path = os.path.join(version_target_path, om_module, "__init__.py")
        with open(init_file_path, "r") as fp:
            content = fp.read()
        with open(init_file_path, "w") as fp:
            om_module_header = [
                "import sys\n",
                "from fairgraph.introspection import (\n",
                "    list_kg_classes as _lkgc,\n",
                "    list_embedded_metadata_classes as _lemc,\n",
                "    set_error_handling as _seh,\n",
                ")\n\n",
            ]
            fp.writelines(om_module_header)
            fp.write(content)
            fp.write(om_module_functions)

    # Write version-level __init__.py
    version_init_path = os.path.join(version_target_path, "__init__.py")
    sorted_modules = sorted(openminds_modules)
    with open(version_init_path, "w") as fp:
        fp.write(f"from . import ({', '.join(sorted_modules)})\n\n\n")
        fp.write("def set_error_handling(value):\n")
        fp.write(
            '    """Set error handling for all openMINDS ' f'{openminds_version} classes, across every submodule."""\n'
        )
        fp.write(f"    for module in ({', '.join(sorted_modules)}):\n")
        fp.write("        module.set_error_handling(value)\n")

    return openminds_modules


def main(openminds_root, version="v4", ignore=[]):
    target_path = os.path.join("..", "fairgraph", "openminds")
    os.makedirs(target_path, exist_ok=True)

    openminds_modules = generate_version(openminds_root, version, target_path)

    # Format with Black
    version_target_path = os.path.join(target_path, version)
    subprocess.call([sys.executable, "-m", "black", "--quiet", version_target_path])

    return openminds_modules


def generate_all(v4_root, v5_root):
    """Generate both v4 and v5 in sequence, then write top-level files."""
    target_path = os.path.join("..", "fairgraph", "openminds")
    os.makedirs(target_path, exist_ok=True)

    v4_modules = generate_version(v4_root, "v4", target_path)
    v5_modules = generate_version(v5_root, "v5", target_path)

    # Write backward-compat alias modules at top level
    with open(os.path.join(target_path, "controlledterms.py"), "w") as fp:
        fp.writelines(
            [
                "from warnings import warn\n"
                "from .controlled_terms import *\n"
                "warn('The `controlledterms` module has been renamed to `controlled_terms`, please update your code', DeprecationWarning)"
            ]
        )
    with open(os.path.join(target_path, "specimenprep.py"), "w") as fp:
        fp.writelines(
            [
                "from warnings import warn\n"
                "from .specimen_prep import *\n"
                "warn('The `specimenprep` module has been renamed to `specimen_prep`, please update your code', DeprecationWarning)"
            ]
        )

    # Format with Black
    subprocess.call([sys.executable, "-m", "black", "--quiet", target_path])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Generate fairgraph classes from the EBRAINS openMINDS schema templates",
    )
    parser.add_argument("openminds_root", help="The path to the openMINDS schema directory")
    parser.add_argument("--version", help="openMINDS version (v4 or v5)", default="v4", choices=["v4", "v5"])
    parser.add_argument("--ignore", help="Names of schema groups to ignore", default=[], action="append")
    parser.add_argument(
        "--v5-root",
        help="Path to v5 schemas (when using --generate-all)",
        default=None,
    )
    parser.add_argument(
        "--generate-all",
        help="Generate both v4 and v5 (requires --v5-root)",
        action="store_true",
    )
    args = parser.parse_args()
    if args.generate_all:
        if args.v5_root is None:
            parser.error("--generate-all requires --v5-root")
        generate_all(args.openminds_root, args.v5_root)
    else:
        main(args.openminds_root, version=args.version, ignore=args.ignore)
