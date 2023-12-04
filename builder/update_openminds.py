import argparse
from collections import defaultdict
from glob import glob
import json
import re
import os
import shutil
import subprocess
import sys

from jinja2 import Environment, select_autoescape, FileSystemLoader


name_map = {
    "shortName": "alias",
    "fullName": "name",
    "scope": "model_scope",
    "hasVersion": "versions",
    "hasEntity": "entities",
    "controlledTerms": "controlledterms",
    "specimenPrep": "specimenprep",
}


reverse_name_map = {
    "RRID": "identifies",
    "about": {
        "https://openminds.ebrains.eu/publications/LearningResource": "learningResource",
        "https://openminds.ebrains.eu/core/Comment": "comment",
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
    "attribute": "isAttributeOf",
    "author": "authored",
    "backgroundStrain": "isBackgroundStrainOf",
    "behavioralProtocol": "usedIn",
    "biologicalSex": "isBiologicalSexOf",
    "breedingType": "isBreedingTypeOf",
    "chemicalProduct": "usedInAmount",
    "citedPublication": "citedIn",
    "commenter": "comment",
    "components": "isComponentOf",  # or "is_part_of" (TODO "components" redundant with "hasComponent"?)
    "conductorMaterial": "isConductorOf",
    "configuration": "isConfigurationOf",
    "constructionType": "usedFor",
    "contactInformation": "isContactInformationOf",
    "contentType": "isDefinedBy",
    "contentTypePattern": "identifiesContentOf",
    "contributor": "contribution",
    "coordinateSpace": "isCoordinateSpaceOf",
    "coordinator": "coordinatedProject",
    "copyOf": "hasCopy",
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
    "descendedFrom": "hasChild",  # equivalent to "hasParent" ?
    "describedIn": "describes",
    "developer": "developed",
    "device": {
        "https://openminds.ebrains.eu/ephys/ElectrodeArrayUsage": "usage",
        "https://openminds.ebrains.eu/ephys/RecordingActivity": "usedIn",
        "https://openminds.ebrains.eu/ephys/ElectrodePlacement": "placedBy",
        "https://openminds.ebrains.eu/ephys/CellPatching": "usedIn",
        "https://openminds.ebrains.eu/ephys/Recording": "usedFor",
        "https://openminds.ebrains.eu/core/Measurement": "usedFor",
    },
    "deviceType": "isTypeOf",  # TODO: replace with "type"?
    "digitalIdentifier": "identifies",
    "diseaseModel": "isModeledBy",
    "editor": "edited",
    "educationalLevel": "appliesTo",
    "environment": "usedFor",  # or "isEnvironmentOf"
    "environmentVariable": "definesEnvironmentOf",
    "ethicsAssessment": "appliesTo",
    "experimentalApproach": "usedIn",
    "feature": "characterizes",
    "fileRepository": "files",
    "format": "isFormatOf",
    "fullDocumentation": "fullyDocuments",
    "funder": "funded",
    "funding": "funded",
    "geneticStrainType": "isGeneticStrainTypeOf",  # or "strain"
    "groupedBy": "isUsedToGroup",
    "groupingType": {
        "https://openminds.ebrains.eu/core/FileBundle": "isUsedToGroup",
        "https://openminds.ebrains.eu/core/FilePathPattern": "isDefinedBy",
    },
    "handedness": "subjectStates",  # or "isHandednessOf"
    "hardware": "usedBy",  # or "isPartOfEnvironment"
    "hasComponent": "isPartOf",
    "hasEntity": "isPartOf",
    "hasParent": "hasChild",  # equivalent to "descendedFrom"
    "hasPart": "isPartOf",
    "hasVersion": "isVersionOf",
    "holder": "holdsCopyright",  # or "intellectualProperty",
    "hostedBy": "hosts",
    "inRelationTo": "assessment",  # equivalent to "about" ?
    "input": "isInputTo",
    "inputData": "isInputTo",  # could use just "input" ?
    "inputFormat": "isInputFormatOf",
    "inspiredBy": "inspired",
    "insulatorMaterial": "composes",
    "isAlternativeVersionOf": "isAlternativeVersionOf",  # ??!!
    "isNewVersionOf": "isOldVersionOf",
    "isPartOf": "hasPart",  # hasComponent ?
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
    "memberOf": "hasMember",
    "metadataLocation": "describes",
    "minValueUnit": "range",
    "maxValueUnit": "range",
    "molecularEntity": "composes",
    "nativeUnit": "usedBy",
    "operatingSystem": "usedBy",
    "origin": "sample",
    "output": "isOutputOf",  # or "generatedBy"
    "outputData": "isOutputOf",  # replace with "output"?
    "outputFormat": "isOutputFormatOf",
    "owner": "isOwnerOf",  # or "devices"
    "pathology": "specimenState",
    "performedBy": "activity",
    "pipetteSolution": "usedIn",
    "preferredDisplayColor": "preferredBy",
    "preparationDesign": "usedFor",
    "previewImage": "isPreviewOf",
    "previousRecording": "nextRecording",
    "productSource": "isSourceOf",
    "programmingLanguage": "usedIn",
    "protocol": "usedIn",
    "provider": "isProviderOf",  # or "provided",
    "publisher": "published",
    "qualitativeOverlap": "assessment",
    "recipe": "defined",  # or "defines"
    "recordedWith": "usedToRecord",
    "referenceData": "isReferenceFor",
    "referenceDataAcquisition": "isReferenceFor",
    "reinforcementType": "usedFor",
    "relatedPublication": "relatedTo",
    "relatedUBERONTerm": "defines",
    "relevantFor": "hasProperties",
    "repository": "containsContentOf",
    "scope": "isScopeOf",
    "scoreType": "isScoreTypeOf",
    "serializationFormat": "usedBy",
    "service": {
        "https://openminds.ebrains.eu/core/ServiceLink": "linkedFrom",
        "https://openminds.ebrains.eu/core/AccountInformation": "hasAccount",
    },
    "setup": "usedIn",
    "slicingDevice": "usedIn",  # TODO: slicingDevice --> device?
    "slicingPlane": "usedIn",
    "software": "usedIn",
    "sourceData": "isSourceDataOf",
    "specialUsageRole": "file",
    "species": "isSpeciesOf",
    "specification": "specifies",
    "specificationFormat": "isSpecificationFormatOf",
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
    "targetIdentificationType": "isTypeOf",
    "technique": "usedIn",
    "tissueBathSolution": "usedIn",
    "type": "isTypeOf",
    "typeOfUncertainty": "value",
    "unit": {
        "https://openminds.ebrains.eu/ephys/Channel": "usedIn",
        "https://openminds.ebrains.eu/core/QuantitativeValue": "value",
        "https://openminds.ebrains.eu/core/QuantitativeValueArray": "value",
    },
    "usedSpecies": "commonCoordinateSpace",
    "usedSpecimen": "usedIn",
    "variation": "usedIn",
    "vendor": "stocks",
    "wasInformedBy": "informed",
}


def generate_python_name(json_name):
    if json_name in name_map:
        python_name = name_map[json_name]
    else:
        python_name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", json_name)
        python_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", python_name).lower()
        python_name = python_name.replace("-", "_")
    return python_name


def generate_doc(property, obj_title):
    if obj_title.upper() == obj_title:  # for acronyms, e.g. DOI
        obj_title_readable = obj_title
    elif "UBERON" in obj_title:
        obj_title_readable = obj_title
    else:
        obj_title_readable = re.sub("([A-Z])", " \g<0>", obj_title).strip().lower()
    doc = property.get("description", "no description available")
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
    "chemicals": {"default": "dataset"},
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
    "controlledterms": {"default": "controlled"},
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
    "chemicals": {"default": "in-depth"},
    "specimenprep": {"default": "in-depth"},
    "stimulation": {"default": "in-depth"},
}


def get_default_space(schema_group, cls_name):
    if schema_group not in DEFAULT_SPACES:
        raise Exception(f"Please update DEFAULT_SPACES for the {schema_group} module")
    if cls_name in DEFAULT_SPACES[schema_group]:
        return DEFAULT_SPACES[schema_group][cls_name]
    else:
        try:
            return DEFAULT_SPACES[schema_group]["default"]
        except KeyError:
            raise KeyError(f"An entry for '{cls_name}' is missing from DEFAULT_SPACES['{schema_group}']")


# in general, we use the required fields when deciding whether a given object already exists
# in the KG. Sometimes this method is inappropriate or undesired, and so for some classes
# we use a custom set of fields.
custom_existence_queries = {
    "LaunchConfiguration": ("executable", "name"),
    "Person": ("given_name", "family_name"),
    "File": ("iri", "hash"),
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
    "Dataset": ("alias",),
    "DatasetVersion": ("alias", "version_identifier"),
    "MetaDataModel": ("alias",),
    "MetaDataModelVersion": ("alias", "version_identifier"),
    "Model": ("name",),  # here we use 'name' instead of 'alias' for backwards compatibility
    "ModelVersion": ("name", "version_identifier"),
    "Project": ("alias",),
    "Software": ("alias",),
    "SoftwareVersion": ("alias", "version_identifier"),
    "Protocol": ("name",),
    "BrainAtlas": ("digital_identifier",),
    "BrainAtlasVersion": ("alias", "version_identifier"),
    "CommonCoordinateSpace": ("alias", "version_identifier"),
    "ParcellationEntity": ("name",),
    "ParcellationEntityVersion": ("name", "version_identifier"),
    "ParcellationTerminologyVersion": ("alias", "version_identifier"),
    "CustomCoordinateSpace": ("name",),
    "WorkflowRecipe": ("name",),
    "WorkflowRecipeVersion": ("name", "version_identifier"),
    "ValidationTest": ("name", "alias"),
    "ValidationTestVersion": ("alias", "version_identifier"),
    "LivePaper": ("name", "alias"),
    "LivePaperVersion": ("alias", "version_identifier"),
    "LivePaperResourceItem": ("name", "iri", "is_part_of"),
    "ScholarlyArticle": ("name",),
    "WorkflowExecution": ("stages",),
    "Configuration": ("configuration",),
    "Periodical": ("abbreviation",),
}


def get_existence_query(cls_name, fields):
    if cls_name in custom_existence_queries:
        return custom_existence_queries[cls_name]

    for field in fields:
        if field["name"] == "lookup_label":
            return ("lookup_label",)

    required_field_names = []
    for field in fields:
        if field["required"]:
            required_field_names.append(field["name"])
    return tuple(required_field_names)


def property_name_sort_key(property):
    """Sort the name field to be first"""
    name = property["name"]
    priorities = {
        "name": "0",
        "alias": "1",
        "lookup_label": "3",
    }
    return priorities.get(name, name)


def generate_class_name(iri):
    assert isinstance(iri, str)
    parts = iri.split("/")[-2:]
    for i in range(len(parts) - 1):
        parts[i] = parts[i].lower()
    return "openminds." + ".".join(parts)


class FairgraphClassBuilder:
    """docstring"""

    def __init__(self, schema_file_path: str, root_path: str, target_path_root: str):
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

    def _target_file_without_extension(self) -> str:
        return os.path.join(*self.relative_path_without_extension)

    def translate(self, embedded=None, linked=None):
        def get_type(property):
            type_map = {
                "string": "str",
                "integer": "int",
                "number": "float",
                "date": "date",
                "date-time": "datetime",
                "time": "time",
                "iri": "IRI",
                "email": "str",  # todo: add an Email class for validation?
                "ECMA262": "str",  #       ...
            }
            if "_linkedTypes" in property:
                types = []
                for item in property["_linkedTypes"]:
                    openminds_module, class_name = item.split("/")[-2:]
                    openminds_module = generate_python_name(openminds_module)
                    types.append(f"openminds.{openminds_module}.{class_name}")
                if len(types) == 1:
                    types = f'"{types[0]}"'
                return types
            elif "_embeddedTypes" in property:
                types = []
                for item in property["_embeddedTypes"]:
                    openminds_module, class_name = item.split("/")[-2:]
                    openminds_module = generate_python_name(openminds_module)
                    types.append(f"openminds.{openminds_module}.{class_name}")
                if len(types) == 1:
                    types = f'"{types[0]}"'
                return types
            elif "type" in property:
                if isinstance(property["type"], list):
                    return [type_map[item] for item in property["type"]]
                else:
                    if property["type"] == "array":
                        return type_map[property["items"]["type"]]
                    elif "_formats" in property:
                        assert isinstance(property["_formats"], list)
                        if len(property["_formats"]) > 1:
                            types = f"[{', '.join([type_map[p] for p in property['_formats']])}]"
                            return types
                        return type_map[property["_formats"][0]]
                    else:
                        return type_map[property["type"]]

            else:
                raise NotImplementedError

        class_name = self._schema_payload["name"]
        module_name = self.relative_path_without_extension[0]
        if self._schema_payload["_type"] in embedded:
            base_class = "EmbeddedMetadata"
            default_space = None
            standard_init_fields = ""
        else:
            base_class = "KGObject"
            default_space = get_default_space(module_name, class_name)
            standard_init_fields = "id=id, space=space, scope=scope, "
        properties = []
        for iri, property in self._schema_payload["properties"].items():
            allow_multiple = property.get("type", "") == "array"
            if allow_multiple:
                property_name = property["namePlural"]
            else:
                property_name = property["name"]
            properties.append(
                {
                    "name": generate_python_name(property_name),
                    "type_str": get_type(property),  # compress using JSON-LD context
                    "iri": f"vocab:{property['name']}",
                    "allow_multiple": allow_multiple,
                    "required": iri in self._schema_payload.get("required", []),
                    "doc": generate_doc(property, class_name),
                    # "instructions": property.get("_instruction", "no instructions available"),
                    "formatting": property.get("formatting", None),
                    "multiline": property.get("multiline", None),
                    "unique_items": property.get("uniqueItems", False),
                    "min_items": property.get("minItems", None),
                    "max_items": property.get("maxItems", None),
                }
            )
        reverse_properties = []
        if linked:
            linked_from = linked[self._schema_payload["_type"]]
            for reverse_link_name in linked_from:
                unique_forward_link_names = set(linked_from[reverse_link_name][0])
                types_str = [generate_class_name(iri) for iri in linked_from[reverse_link_name][2]]
                if len(unique_forward_link_names) == 1:
                    (forward_link_name,) = unique_forward_link_names
                    (forward_link_name_plural,) = set(linked_from[reverse_link_name][1])
                    _forward_link_name_python = generate_python_name(forward_link_name_plural)
                    iri = f"^vocab:{forward_link_name}"
                    doc = f"reverse of '{forward_link_name}'"  # use _plural?
                    types_str = sorted(types_str)
                    if len(types_str) == 1:
                        types_str = f'"{types_str[0]}"'
                else:
                    backwards_compatible = True
                    if backwards_compatible:
                        forward_link_name = sorted(set(linked_from[reverse_link_name][0]))
                        forward_link_name_plural = sorted(set(linked_from[reverse_link_name][1]))
                        types_str = sorted(types_str)
                    else:
                        # this is a better solution, since we keep the match between types and names
                        # in the order of the lists, but is not backwards compatible
                        forward_link_name = linked_from[reverse_link_name][0]
                        forward_link_name_plural = linked_from[reverse_link_name][1]
                    _forward_link_name_python = [generate_python_name(name) for name in forward_link_name_plural]
                    iri = [f"^vocab:{name}" for name in forward_link_name]
                    doc = "reverse of " + ", ".join(name for name in forward_link_name)  # use _plural?
                reverse_properties.append(
                    {
                        "name": generate_python_name(reverse_link_name),
                        "type_str": types_str,
                        "_forward_name_python": _forward_link_name_python,
                        "iri": iri,
                        "allow_multiple": True,
                        "required": False,
                        "doc": doc,
                    }
                )
        self.context = {
            "docstring": self._schema_payload.get("description", "<description not available>"),
            "base_class": base_class,
            "preamble": "",  # default value, may be updated below
            "class_name": class_name,
            "default_space": default_space,
            "openminds_type": self._schema_payload["_type"],
            "fields": sorted(properties, key=property_name_sort_key),
            "reverse_fields": sorted(reverse_properties, key=property_name_sort_key),
            "additional_methods": "",
            "existence_query_fields": get_existence_query(class_name, properties),
            "standard_init_fields": standard_init_fields,
        }
        import_map = {
            "date": "from datetime import date",
            "datetime": "from datetime import datetime",
            "time": "from datetime import time",
            "IRI": "from openminds.base import IRI",
            "[datetime, time]": "from datetime import datetime, time",
        }
        extra_imports = set()
        for property in self.context["fields"]:
            if isinstance(property["type_str"], list):
                for t in property["type_str"]:
                    imp = import_map.get(t, None)
                    if imp:
                        extra_imports.add(imp)
            else:
                imp = import_map.get(property["type_str"], None)
                if imp:
                    extra_imports.add(imp)
            if extra_imports:
                self.context["preamble"] = "\n".join(sorted(extra_imports))

    def build(self, embedded=None, linked=None):
        target_file_path = os.path.join(self.target_path_root, f"{self._target_file_without_extension()}.py")
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        self.translate(embedded=embedded, linked=linked)

        with open(target_file_path, "w") as target_file:
            contents = self.env.get_template(self.template_name).render(self.context)
            target_file.write(contents)

        return (self._target_file_without_extension().replace("/", "."), self.context["class_name"])

    def get_edges(self):
        embedded = set()
        linked = {}
        for property in self._schema_payload["properties"].values():
            for emb in property.get("_embeddedTypes", []):
                embedded.add(emb)
            for lnk in property.get("_linkedTypes", []):
                reverse_link_name = property["nameForReverseLink"]
                if reverse_link_name is None:
                    reverse_link_name = reverse_name_map[property["name"]]
                linked[lnk] = (
                    self._schema_payload["_type"],
                    property["name"],
                    property["namePlural"],
                    reverse_link_name,
                )  # linked from (cls, property name, property name plural, reverse name)
        return embedded, linked


def main(openminds_root, ignore=[]):
    target_path = os.path.join("..", "fairgraph", "openminds")
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    openminds_root = os.path.realpath(openminds_root)

    schema_file_paths = glob(os.path.join(openminds_root, f"**/*.schema.omi.json"), recursive=True)
    python_modules = defaultdict(list)

    # First pass - figure out which schemas are embedded and which are linked
    embedded = set()
    linked = defaultdict(dict)
    for schema_file_path in schema_file_paths:
        embedded_in, linked_from = FairgraphClassBuilder(schema_file_path, openminds_root, target_path).get_edges()
        embedded.update(embedded_in)
        for openminds_type, (link_type, property_name, property_name_plural, reverse_name) in linked_from.items():
            if isinstance(reverse_name, dict):
                print("todo")
                continue
            if link_type not in embedded:
                if reverse_name in linked[openminds_type]:
                    linked[openminds_type][reverse_name][0].append(property_name)
                    linked[openminds_type][reverse_name][1].append(property_name_plural)
                    linked[openminds_type][reverse_name][2].append(link_type)
                else:
                    linked[openminds_type][reverse_name] = ([property_name], [property_name_plural], [link_type])
    conflicts = set(linked).intersection(embedded)
    if conflicts:
        print(f"Found schema(s) that are both linked and embedded: {conflicts}")
        # conflicts should not happen in new versions.
        for schema_identifier in conflicts:
            linked.pop(schema_identifier, None)

    # Second pass - create a Python module for each openMINDS schema
    for schema_file_path in schema_file_paths:
        module_path, class_name = FairgraphClassBuilder(schema_file_path, openminds_root, target_path).build(
            embedded=embedded, linked=linked
        )

        parts = module_path.split(".")
        parent_path = ".".join(parts[:-1])
        python_modules[parent_path].append((parts[-1], class_name))

    # Now create additional files, e.g. __init__.py
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))), autoescape=select_autoescape()
    )
    openminds_modules = set()
    for path, classes in python_modules.items():
        dir_path = path.split(".")
        openminds_modules.add(dir_path[0])
        init_file_path = os.path.join(target_path, *(dir_path + ["__init__.py"]))
        with open(init_file_path, "w") as fp:
            contents = env.get_template("init_template.py.txt").render({"classes": sorted(classes)})
            fp.write(contents)
        while len(dir_path) > 1:
            child_dir = dir_path[-1]
            dir_path = dir_path[:-1]
            init_file_path = os.path.join(target_path, *(dir_path + ["__init__.py"]))
            with open(init_file_path, "a") as fp:
                if len(dir_path) > 0:
                    class_names = ", ".join(class_name for _, class_name in classes)
                    fp.write(f"from .{child_dir} import ({class_names})\n")

    init_file_path = os.path.join("..", "fairgraph", "openminds", "__init__.py")
    with open(init_file_path, "w") as fp:
        fp.write(f"from . import ({', '.join(sorted(openminds_modules))})\n")

    # Format with Black
    subprocess.call([sys.executable, "-m", "black", "--quiet", target_path])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Generate fairgraph classes from the EBRAINS openMINDS schema templates",
    )
    parser.add_argument("openminds_root", help="The path to the openMINDS directory")
    parser.add_argument("--ignore", help="Names of schema groups to ignore", default=[], action="append")
    args = vars(parser.parse_args())
    main(**args)
