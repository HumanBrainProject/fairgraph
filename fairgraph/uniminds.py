"""
An updated version of MINDS

"""

# Copyright 2019 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys, inspect
from datetime import datetime
try:
    basestring
except NameError:
    basestring = str

from fairgraph.base import KGObject, KGProxy, KGQuery, cache, as_list, Field
from fairgraph.data import FileAssociation, CSCSFile
from fairgraph.commons import QuantitativeValue
from fairgraph.minds import MINDSObject

class UnimindsObject(MINDSObject):
    namespace = "uniminds"


class UnimindsOption(MINDSObject):
    namespace = "uniminds"


class Person(UnimindsObject):
    """
    A person associated with research data or models, for example as an experimentalist,
    or a data analyst.
    """
    _path = "/core/person/v1.0.0"
    type = ["uniminds:Person"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("email", basestring, "http://schema.org/email", required=False, multiple=False),
      Field("family_name", basestring, "http://schema.org/familyName", required=False, multiple=False),
      Field("given_name", basestring, "http://schema.org/givenName", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("orcid", basestring, "https://schema.hbp.eu/uniminds/orcid", required=False, multiple=False))
    existence_query_fields = ("family_name", "given_name")

class AbstractionLevel(UnimindsOption):
    """
    Level of abstraction for a neuroscience model, e.g.rate neurons, spiking neurons
    """
    _path = "/options/abstractionlevel/v1.0.0"
    type = ["uniminds:Abstractionlevel"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class AgeCategory(UnimindsOption):
    """
    An age category, e.g. "adult", "juvenile"
    """
    _path = "/options/agecategory/v1.0.0"
    type = ["uniminds:Agecategory"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class BrainStructure(UnimindsOption):
    """
    A sub-structure or region with the brain.
    """
    _path = "/options/brainstructure/v1.0.0"
    type = ["uniminds:Brainstructure"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class CellularTarget(UnimindsOption):
    """
    The type of neuron or glial cell that is the focus of the study.
    """
    _path = "/options/cellulartarget/v1.0.0"
    type = ["uniminds:Cellulartarget"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Country(UnimindsOption):
    """
    A geographical country.
    """
    _path = "/options/country/v1.0.0"
    type = ["uniminds:Country"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Dataset(UnimindsObject):
    """
    A collection of related data files.
    """
    _path = "/core/dataset/v1.0.0"
    type = ["uniminds:Dataset"]
    fields = (
      #Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("intended_release_date", datetime, "https://schema.hbp.eu/uniminds/intendedReleaseDate", required=False, multiple=False),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("brain_structure", BrainStructure, "https://schema.hbp.eu/uniminds/brainStructure", required=False, multiple=False),
      Field("cellular_target", CellularTarget, "https://schema.hbp.eu/uniminds/cellularTarget", required=False, multiple=False),
      Field("contributor", Person, "https://schema.hbp.eu/uniminds/contributor", required=False, multiple=True),
      #Field("created_as", basestring, "https://schema.hbp.eu/uniminds/createdAs", required=False, multiple=False),
      Field("custodian", Person, "https://schema.hbp.eu/uniminds/custodian", required=False, multiple=True),
      Field("doi", "uniminds.Doi", "https://schema.hbp.eu/uniminds/doi", required=False, multiple=False),
      Field("embargo_status", "uniminds.EmbargoStatus", "https://schema.hbp.eu/uniminds/embargoStatus", required=False, multiple=False),
      Field("ethics_approval", "uniminds.EthicsApproval", "https://schema.hbp.eu/uniminds/ethicsApproval", required=False, multiple=False),
      Field("funding_information", "uniminds.FundingInformation", "https://schema.hbp.eu/uniminds/fundingInformation", required=False, multiple=False),
      Field("hbp_component", "uniminds.HBPComponent", "https://schema.hbp.eu/uniminds/hbpComponent", required=False, multiple=False),
      Field("license", "uniminds.License", "https://schema.hbp.eu/uniminds/license", required=False, multiple=False),
      Field("main_contact", Person, "https://schema.hbp.eu/uniminds/mainContact", required=False, multiple=True),
      Field("main_file_bundle", "uniminds.FileBundle", "https://schema.hbp.eu/uniminds/mainFileBundle", required=False, multiple=True),
      Field("method", "uniminds.Method", "https://schema.hbp.eu/uniminds/method", required=False, multiple=True),
      Field("project", "uniminds.Project", "https://schema.hbp.eu/uniminds/project", required=False, multiple=False),
      Field("publication", "uniminds.Publication", "https://schema.hbp.eu/uniminds/publication", required=False, multiple=True),
      Field("species", "uniminds.Species", "https://schema.hbp.eu/uniminds/species", required=False, multiple=False),
      Field("study_target", "uniminds.StudyTarget", "https://schema.hbp.eu/uniminds/studyTarget", required=False, multiple=False),
      Field("subjectgroup", "uniminds.SubjectGroup", "https://schema.hbp.eu/uniminds/subjectGroup", required=False, multiple=True))



class Disability(UnimindsOption):
    """
    A disability or disease.
    """
    _path = "/options/disability/v1.0.0"
    type = ["uniminds:Disability"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Doi(UnimindsOption):
    """
    Digital Object Identifier (https://www.doi.org)
    """
    _path = "/options/doi/v1.0.0"
    type = ["uniminds:Doi"]
    fields = (
      Field("citation", basestring, "https://schema.hbp.eu/uniminds/citation", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class EmbargoStatus(UnimindsOption):
    """
    Information about the embargo period during which a given dataset cannot be publicly shared.
    """
    _path = "/options/embargostatus/v1.0.0"
    type = ["uniminds:Embargostatus"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class EthicsApproval(UnimindsObject):
    """
    Record of an  ethics approval.
    """
    _path = "/core/ethicsapproval/v1.0.0"
    type = ["uniminds:Ethicsapproval"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("hbpethicsapproval", basestring, "https://schema.hbp.eu/uniminds/hbpEthicsApproval", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("country_of_origin", Country, "https://schema.hbp.eu/uniminds/countryOfOrigin", required=False, multiple=False),
      Field("ethics_authority", "uniminds.EthicsAuthority", "https://schema.hbp.eu/uniminds/ethicsAuthority", required=False, multiple=True))



class EthicsAuthority(UnimindsOption):
    """
    A entity legally authorised to approve or deny permission to conduct an experiment on ethical grounds.
    """
    _path = "/options/ethicsauthority/v1.0.0"
    type = ["uniminds:Ethicsauthority"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class ExperimentalPreparation(UnimindsOption):
    """
    An experimental preparation.
    """
    _path = "/options/experimentalpreparation/v1.0.0"
    type = ["uniminds:Experimentalpreparation"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class File(UnimindsObject):
    """
    Metadata about a single file.
    """
    _path = "/core/file/v1.0.0"
    type = ["uniminds:File"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("url", basestring, "http://schema.org/url", required=False, multiple=False),
      Field("mime_type", "uniminds.MimeType", "https://schema.hbp.eu/uniminds/mimeType", required=False, multiple=False))


class FileAssociation(UnimindsObject):
    """
    A link between a file and a dataset.
    """
    _path = "/core/fileassociation/v1.0.0"
    type = ["uniminds:Fileassociation"]
    fields = (
      Field("from", File, "https://schema.hbp.eu/linkinginstance/from", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("to", Dataset, "https://schema.hbp.eu/linkinginstance/to", required=False, multiple=False))


class FileBundle(UnimindsObject):
    """
    A collection of files (e.g. in a folder or directory structure)
    """
    _path = "/core/filebundle/v1.0.0"
    type = ["uniminds:FileBundle"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("url", basestring, "http://schema.org/url", required=False, multiple=False),
      Field("usage_notes", basestring, "https://schema.hbp.eu/uniminds/usageNotes", required=False, multiple=False),
      Field("file", File, "https://schema.hbp.eu/uniminds/file", required=False, multiple=False),
      Field("file_bundle", "uniminds.FileBundle", "https://schema.hbp.eu/uniminds/fileBundle", required=False, multiple=False),
      Field("mime_type", "uniminds.MimeType", "https://schema.hbp.eu/uniminds/mimeType", required=False, multiple=True),
      Field("model_instance", "uniminds.ModelInstance", "https://schema.hbp.eu/uniminds/modelInstance", required=False))


class FileBundleGroup(UnimindsObject):
    """
    A collection of file bundles (see :class:`FileBundle`)
    """
    _path = "/options/filebundlegroup/v1.0.0"
    type = ["uniminds:Filebundlegroup"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))



class FundingInformation(UnimindsObject):
    """
    Information about the source of funding of a study.
    """
    _path = "/core/fundinginformation/v1.0.0"
    type = ["uniminds:Fundinginformation"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("grant_id", basestring, "https://schema.hbp.eu/uniminds/grantId", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Genotype(UnimindsOption):
    """
    Genetic makeup of a study subject, typically a reference to an inbred strain,
    with or without mutations.
    """
    _path = "/options/genotype/v1.0.0"
    type = ["uniminds:Genotype"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Handedness(UnimindsOption):
    """
    Preferred hand (left, right, or ambidextrous)
    """
    _path = "/options/handedness/v1.0.0"
    type = ["uniminds:Handedness"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class HBPComponent(UnimindsObject):
    """
    A data or software component, as defined in the HBP "project lifecycle" application.
    """
    _path = "/core/hbpcomponent/v1.0.0"
    type = ["uniminds:Hbpcomponent"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("associated_task", basestring, "https://schema.hbp.eu/uniminds/associatedTask", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("component_owner", Person, "https://schema.hbp.eu/uniminds/componentOwner", required=False, multiple=False))


class License(UnimindsOption):
    """
    A license governing sharing of a dataset.
    """
    _path = "/options/license/v1.0.0"
    type = ["uniminds:License"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("fullname", basestring, "https://schema.hbp.eu/uniminds/fullName", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("url", basestring, "http://schema.org/url", required=False, multiple=False))


class Method(UnimindsObject):
    """
    An experimental method.
    """
    _path = "/core/method/v1.0.0"
    type = ["uniminds:Method"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("fullname", basestring, "https://schema.hbp.eu/uniminds/fullName", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("brain_structure", BrainStructure, "https://schema.hbp.eu/uniminds/brainStructure", required=False, multiple=True),
      Field("ethics_approval", EthicsApproval, "https://schema.hbp.eu/uniminds/ethicsApproval", required=False, multiple=False),
      Field("experimental_preparation", ExperimentalPreparation, "https://schema.hbp.eu/uniminds/experimentalPreparation", required=False, multiple=False),
      Field("method_category", "uniminds.MethodCategory", "https://schema.hbp.eu/uniminds/methodCategory", required=False, multiple=False),
      Field("publication", "uniminds.Publication", "https://schema.hbp.eu/uniminds/publication", required=False, multiple=False),
      Field("study_target", "uniminds.StudyTarget", "https://schema.hbp.eu/uniminds/studyTarget", required=False, multiple=False),
      Field("submethod", "uniminds.Method", "https://schema.hbp.eu/uniminds/subMethod", required=False, multiple=True))


class MethodCategory(UnimindsOption):
    """
    A category used for classifying experimental methods (see :class:`ExperimentalMethod`)
    """
    _path = "/options/methodcategory/v1.0.0"
    type = ["uniminds:Methodcategory"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class MimeType(UnimindsOption):
    """
    Media type of a document
    """
    _path = "/options/mimetype/v1.0.0"
    type = ["uniminds:Mimetype"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class ModelFormat(UnimindsOption):
    """
    Programming or markup language used to describe or create a model
    """
    _path = "/options/modelformat/v1.0.0"
    type = ["uniminds:Modelformat"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class ModelInstance(UnimindsObject):
    """
    A specific version/parameterization of a neuroscience model.
    """
    _path = "/core/modelinstance/v1.0.0"
    type = ["uniminds:Modelinstance"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("license", License, "http://schema.org/license", required=False, multiple=False),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("version", basestring, "http://schema.org/version", required=False, multiple=False),
      Field("abstraction_level", AbstractionLevel, "https://schema.hbp.eu/uniminds/abstractionLevel", required=False, multiple=False),
      Field("brain_structure", BrainStructure, "https://schema.hbp.eu/uniminds/brainStructure", required=False, multiple=True),
      Field("cellular_target", CellularTarget, "https://schema.hbp.eu/uniminds/cellularTarget", required=False, multiple=True),
      Field("contributor", Person, "https://schema.hbp.eu/uniminds/contributor", required=False, multiple=True),
      Field("custodian", Person, "https://schema.hbp.eu/uniminds/custodian", required=False, multiple=True),
      Field("main_contact", Person, "https://schema.hbp.eu/uniminds/mainContact", required=False, multiple=True),
      Field("used_dataset", KGObject, "https://schema.hbp.eu/uniminds/usedDataset", required=False, multiple=True),
      Field("produced_dataset", Dataset, "https://schema.hbp.eu/uniminds/producedDataset", required=False, multiple=True),
      Field("modelformat", ModelFormat, "https://schema.hbp.eu/uniminds/modelFormat", required=False, multiple=True),
      Field("modelscope", "uniminds.ModelScope", "https://schema.hbp.eu/uniminds/modelScope", required=False, multiple=False),
      Field("publication", "uniminds.Publication", "https://schema.hbp.eu/uniminds/publication", required=False, multiple=False),
      Field("study_target", "uniminds.StudyTarget", "https://schema.hbp.eu/uniminds/studyTarget", required=False, multiple=True),
      Field("embargo_status", "uniminds.EmbargoStatus", "https://schema.hbp.eu/uniminds/embargoStatus", required=False, multiple=False),
      Field("alternate_of", ["brainsimulation.ModelInstance", "brainsimulation.MEModel"], "^prov:alternateOf",
            reverse="alternate_of")
    )
    existence_query_fields = ["identifier"]

    def contributor_names(self, client, api="query"):
        names = []
        for person in as_list(self.contributor):
            person = person.resolve(client, api=api)
            if person:
                names.append(person.name)
            else:
                pass  # todo: warning
        return ", ".join(names)


class ModelScope(UnimindsOption):
    """
    'What is being modelled': a protein, a single cell, the entire brain, etc.
    """
    _path = "/options/modelscope/v1.0.0"
    type = ["uniminds:Modelscope"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Organization(UnimindsObject):
    """
    An organization associated with research data or models, e.g. a university, lab or department.
    """
    _path = "/options/organization/v1.0.0"
    type = ["uniminds:Organization"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("created_as", basestring, "https://schema.hbp.eu/uniminds/createdAs", required=False, multiple=False))


class Project(UnimindsObject):
    """
    A research project, which may have generated one or more datasets (see :class:`Dataset`)
    """
    _path = "/core/project/v1.0.0"
    type = ["uniminds:Project"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("coordinator", Person, "https://schema.hbp.eu/uniminds/coordinator", required=False, multiple=True))


class Publication(UnimindsObject):
    """
    A scientific publication.
    """
    _path = "/core/publication/v1.0.0"
    type = ["uniminds:Publication"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("url", basestring, "http://schema.org/url", required=False, multiple=False),
      Field("brain_structure", BrainStructure, "https://schema.hbp.eu/uniminds/brainStructure", required=False, multiple=False),
      Field("project", Project, "https://schema.hbp.eu/uniminds/project", required=False, multiple=False),
      Field("publication_id", "uniminds.PublicationId", "https://schema.hbp.eu/uniminds/publicationId", required=False, multiple=False),
      Field("study_target", "uniminds.StudyTarget", "https://schema.hbp.eu/uniminds/studyTarget", required=False, multiple=False),
      Field("subjectgroup", "uniminds.SubjectGroup", "https://schema.hbp.eu/uniminds/subjectGroup", required=False, multiple=False))


class PublicationId(UnimindsOption):
    """
    Identifier for a publication (e.g. a DOI, a PubMed ID)
    """
    _path = "/options/publicationid/v1.0.0"
    type = ["uniminds:Publicationid"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("publication", Publication, "https://schema.hbp.eu/uniminds/publication", required=False, multiple=False),
      Field("publication_id_type", "uniminds.PublicationIdType", "https://schema.hbp.eu/uniminds/publicationIdType", required=False, multiple=False))


class PublicationIdType(UnimindsOption):
    """
    A type of publication identifier (e.g. ISBN, DOI)
    """
    _path = "/options/publicationidtype/v1.0.0"
    type = ["uniminds:Publicationidtype"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Sex(UnimindsOption):
    """
    The sex of an animal or person from whom/which data were obtained.
    """
    _path = "/options/sex/v1.0.0"
    type = ["uniminds:Sex"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Species(UnimindsOption):
    """
    The species of an experimental subject, expressed with the binomial nomenclature.
    """
    _path = "/options/species/v1.0.0"
    type = ["uniminds:Species"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Strain(UnimindsOption):
    """
    An inbred sub-population within a species.
    """
    _path = "/options/strain/v1.0.0"
    type = ["uniminds:Strain"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class StudyTarget(UnimindsObject):
    """
    The focus of an experimental or modelling study.
    """
    _path = "/core/studytarget/v1.0.0"
    type = ["uniminds:Studytarget"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("fullname", basestring, "https://schema.hbp.eu/uniminds/fullName", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("study_target_source", "uniminds.StudyTargetSource", "https://schema.hbp.eu/uniminds/studyTargetSource", required=False, multiple=False),
      Field("study_target_type", "uniminds.StudyTargetType", "https://schema.hbp.eu/uniminds/studyTargetType", required=False, multiple=False))


class StudyTargetSource(UnimindsOption):
    """
    Context of a study target, e.g. if the target is a brain region, the source might be an atlas.
    """
    _path = "/options/studytargetsource/v1.0.0"
    type = ["uniminds:Studytargetsource"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))



class StudyTargetType(UnimindsOption):
    """
    Category of study target (see :class:`StudyTarget`)
    """
    _path = "/options/studytargettype/v1.0.0"
    type = ["uniminds:Studytargettype"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))



class Subject(UnimindsObject):
    """
    The organism that is the subject of an experimental investigation.
    """
    _path = "/core/subject/v1.0.0"
    type = ["uniminds:Subject"]
    fields = (
      Field("age", (basestring, float), "https://schema.hbp.eu/uniminds/age", required=False, multiple=False),
      Field("age_range_max", (basestring, float), "https://schema.hbp.eu/uniminds/ageRangeMax", required=False, multiple=False),
      Field("age_range_min", (basestring, float), "https://schema.hbp.eu/uniminds/ageRangeMin", required=False, multiple=False),
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("age_category", AgeCategory, "https://schema.hbp.eu/uniminds/ageCategory", required=False, multiple=False),
      Field("brain_structure", BrainStructure, "https://schema.hbp.eu/uniminds/brainstructure", required=False, multiple=False),
      Field("cellular_target", CellularTarget, "https://schema.hbp.eu/uniminds/cellularTarget", required=False, multiple=False),
      Field("disability", Disability, "https://schema.hbp.eu/uniminds/disability", required=False, multiple=False),
      Field("genotype", Genotype, "https://schema.hbp.eu/uniminds/genotype", required=False, multiple=False),
      Field("handedness", Handedness, "https://schema.hbp.eu/uniminds/handedness", required=False, multiple=False),
      #Field("method", Method, "https://schema.hbp.eu/uniminds/method", required=False, multiple=True),
      Field("publication", Publication, "https://schema.hbp.eu/uniminds/publication", required=False, multiple=False),
      Field("sex", Sex, "https://schema.hbp.eu/uniminds/sex", required=False, multiple=False),
      Field("species", Species, "https://schema.hbp.eu/uniminds/species", required=False, multiple=False),
      Field("strain", Strain, "https://schema.hbp.eu/uniminds/strain", required=False, multiple=False),
      Field("study_target", StudyTarget, "https://schema.hbp.eu/uniminds/studyTarget", required=False, multiple=True))


class SubjectGroup(UnimindsObject):
    """
    A group of experimental subjects.
    """
    _path = "/core/subjectgroup/v1.0.0"
    type = ["uniminds:Subjectgroup"]
    fields = (
      Field("age_range_max", (basestring, float), "https://schema.hbp.eu/uniminds/ageRangeMax", required=False, multiple=False),
      Field("age_range_min", (basestring, float), "https://schema.hbp.eu/uniminds/ageRangeMin", required=False, multiple=False),
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("num_of_subjects", int, "https://schema.hbp.eu/uniminds/numOfSubjects", required=False, multiple=False),
      Field("age_category", AgeCategory, "https://schema.hbp.eu/uniminds/ageCategory", required=False, multiple=False),
      Field("cellular_target", CellularTarget, "https://schema.hbp.eu/uniminds/cellularTarget", required=False, multiple=False),
      Field("brain_structure", BrainStructure, "https://schema.hbp.eu/uniminds/brainStructure", required=False, multiple=False),
      Field("disability", Disability, "https://schema.hbp.eu/uniminds/disability", required=False, multiple=False),
      Field("genotype", Genotype, "https://schema.hbp.eu/uniminds/genotype", required=False, multiple=False),
      Field("handedness", Handedness, "https://schema.hbp.eu/uniminds/handedness", required=False, multiple=True),
      #Field("method", Method, "https://schema.hbp.eu/uniminds/method", required=False, multiple=True),
      Field("publication", Publication, "https://schema.hbp.eu/uniminds/publication", required=False, multiple=False),
      Field("sex", Sex, "https://schema.hbp.eu/uniminds/sex", required=False, multiple=True),
      Field("species", Species, "https://schema.hbp.eu/uniminds/species", required=False, multiple=True),
      Field("strain", Strain, "https://schema.hbp.eu/uniminds/strain", required=False, multiple=True),
      Field("study_target", StudyTarget, "https://schema.hbp.eu/uniminds/studyTarget", required=False, multiple=True),
      Field("subjects", Subject, "https://schema.hbp.eu/uniminds/subjects", required=False, multiple=True))



class TissueSample(UnimindsObject):
    """
    A sample of brain tissue.
    """
    _path = "/core/tissuesample/v1.0.0"
    type = ["uniminds:Tissuesample"]
    fields = (
      Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("subject", Subject, "https://schema.hbp.eu/uniminds/subject", required=False, multiple=False))


def list_kg_classes():
    """List all KG classes defined in this module"""
    classes = [obj for name, obj in inspect.getmembers(sys.modules[__name__])
               if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__ == __name__]
    classes.remove(UnimindsObject)
    classes.remove(UnimindsOption)
    return classes


if __name__=='__main__':

    import os
    from fairgraph import uniminds, KGClient
    token = os.environ['HBP_token']
    client = KGClient(token)
    for cls in uniminds.list_kg_classes():
        print(cls.__name__)
        # for f in cls.fields:
        #     print('    - %s' % f.name)
