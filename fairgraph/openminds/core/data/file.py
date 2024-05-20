"""
Structured information on a file instance that is accessible via a URL.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property

import os
import mimetypes
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import quote, urlparse, urlunparse
from .hash import Hash
from .content_type import ContentType
from ..miscellaneous.quantitative_value import QuantitativeValue
from ...controlled_terms.unit_of_measurement import UnitOfMeasurement
from fairgraph.utility import accepted_terms_of_use, sha1sum

mimetypes.init()
from fairgraph.base import IRI


class File(KGObject):
    """
    Structured information on a file instance that is accessible via a URL.
    """

    default_space = "files"
    type_ = "https://openminds.ebrains.eu/core/File"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("content_description", str, "vocab:contentDescription", doc="no description available"),
        Property(
            "data_types",
            "openminds.controlled_terms.DataType",
            "vocab:dataType",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "file_repository", "openminds.core.FileRepository", "vocab:fileRepository", doc="no description available"
        ),
        Property(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Property(
            "hashes",
            "openminds.core.Hash",
            "vocab:hash",
            multiple=True,
            doc="Term used for the process of converting any data into a single value. Often also directly refers to the resulting single value.",
        ),
        Property(
            "iri",
            IRI,
            "vocab:IRI",
            required=True,
            doc="Stands for Internationalized Resource Identifier which is an internet protocol standard that builds on the URI protocol, extending the set of permitted characters to include Unicode/ISO 10646.",
        ),
        Property(
            "is_part_of",
            "openminds.core.FileBundle",
            "vocab:isPartOf",
            multiple=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the file.",
        ),
        Property(
            "special_usage_role",
            "openminds.controlled_terms.FileUsageRole",
            "vocab:specialUsageRole",
            doc="Particular function of something when it is used.",
        ),
        Property(
            "storage_size",
            "openminds.core.QuantitativeValue",
            "vocab:storageSize",
            doc="Quantitative value defining how much disk space is used by an object on a computer system.",
        ),
        Property(
            "describes",
            [
                "openminds.core.BehavioralProtocol",
                "openminds.core.Protocol",
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimen_prep.SlicingDeviceUsage",
            ],
            ["^vocab:describedIn", "^vocab:metadataLocation"],
            reverse=["described_in", "metadata_locations"],
            multiple=True,
            doc="reverse of describedIn, metadataLocation",
        ),
        Property(
            "fully_documents",
            [
                "openminds.core.MetaDataModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebServiceVersion",
                "openminds.publications.LivePaperVersion",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:fullDocumentation",
            reverse="full_documentations",
            multiple=True,
            doc="reverse of 'fullDocumentation'",
        ),
        Property(
            "has_copies",
            "openminds.computation.LocalFile",
            "^vocab:copyOf",
            reverse="copy_of",
            multiple=True,
            doc="reverse of 'copyOf'",
        ),
        Property(
            "is_also_part_of",
            "openminds.computation.WorkflowRecipeVersion",
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Property(
            "is_configuration_of",
            "openminds.computation.WorkflowExecution",
            "^vocab:configuration",
            reverse="configurations",
            multiple=True,
            doc="reverse of 'configuration'",
        ),
        Property(
            "is_default_image_for",
            "openminds.sands.CustomCoordinateSpace",
            "^vocab:defaultImage",
            reverse="default_images",
            multiple=True,
            doc="reverse of 'defaultImage'",
        ),
        Property(
            "is_input_to",
            "openminds.core.DatasetVersion",
            "^vocab:inputData",
            reverse="input_data",
            multiple=True,
            doc="reverse of 'inputData'",
        ),
        Property(
            "is_location_of",
            ["openminds.ephys.Recording", "openminds.sands.ParcellationTerminologyVersion"],
            "^vocab:dataLocation",
            reverse="data_locations",
            multiple=True,
            doc="reverse of 'dataLocation'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
                "openminds.core.ModelVersion",
                "openminds.core.ProtocolExecution",
                "openminds.ephys.RecordingActivity",
            ],
            ["^vocab:output", "^vocab:outputData"],
            reverse=["output_data", "outputs"],
            multiple=True,
            doc="reverse of output, outputData",
        ),
        Property(
            "is_preview_of",
            "openminds.core.ServiceLink",
            "^vocab:previewImage",
            reverse="preview_images",
            multiple=True,
            doc="reverse of 'previewImage'",
        ),
        Property(
            "is_reference_for",
            "openminds.computation.ValidationTestVersion",
            "^vocab:referenceData",
            reverse="reference_data",
            multiple=True,
            doc="reverse of 'referenceData'",
        ),
        Property(
            "is_source_data_of",
            "openminds.core.FileArchive",
            "^vocab:sourceData",
            reverse="source_data",
            multiple=True,
            doc="reverse of 'sourceData'",
        ),
        Property(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
        Property(
            "specifies",
            [
                "openminds.sands.AtlasAnnotation",
                "openminds.sands.CustomAnnotation",
                "openminds.stimulation.EphysStimulus",
            ],
            "^vocab:specification",
            reverse="specifications",
            multiple=True,
            doc="reverse of 'specification'",
        ),
    ]
    aliases = {"hash": "hashes"}
    existence_query_properties = ("iri", "hash")

    def __init__(
        self,
        name=None,
        content_description=None,
        data_types=None,
        describes=None,
        file_repository=None,
        format=None,
        fully_documents=None,
        has_copies=None,
        hash=None,
        hashes=None,
        iri=None,
        is_also_part_of=None,
        is_configuration_of=None,
        is_default_image_for=None,
        is_input_to=None,
        is_location_of=None,
        is_output_of=None,
        is_part_of=None,
        is_preview_of=None,
        is_reference_for=None,
        is_source_data_of=None,
        is_used_to_group=None,
        special_usage_role=None,
        specifies=None,
        storage_size=None,
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
            content_description=content_description,
            data_types=data_types,
            describes=describes,
            file_repository=file_repository,
            format=format,
            fully_documents=fully_documents,
            has_copies=has_copies,
            hash=hash,
            hashes=hashes,
            iri=iri,
            is_also_part_of=is_also_part_of,
            is_configuration_of=is_configuration_of,
            is_default_image_for=is_default_image_for,
            is_input_to=is_input_to,
            is_location_of=is_location_of,
            is_output_of=is_output_of,
            is_part_of=is_part_of,
            is_preview_of=is_preview_of,
            is_reference_for=is_reference_for,
            is_source_data_of=is_source_data_of,
            is_used_to_group=is_used_to_group,
            special_usage_role=special_usage_role,
            specifies=specifies,
            storage_size=storage_size,
        )

    @classmethod
    def from_local_file(cls, relative_path):
        obj = cls(
            name=relative_path,
            storage_size=QuantitativeValue(
                value=float(os.stat(relative_path).st_size), unit=UnitOfMeasurement(name="bytes")
            ),
            hashes=Hash(algorithm="SHA1", digest=sha1sum(relative_path)),
            format=ContentType(name=mimetypes.guess_type(relative_path)[0])
            # todo: query ContentTypes since that contains additional, EBRAINS-specific content types
        )
        return obj

    def download(self, local_path, client, accept_terms_of_use=False):
        if accepted_terms_of_use(client, accept_terms_of_use=accept_terms_of_use):
            local_path = Path(local_path)
            if local_path.is_dir():
                local_filename = local_path / self.name
            else:
                local_filename = local_path
                local_filename.parent.mkdir(parents=True, exist_ok=True)
            url_parts = urlparse(self.iri.value)
            url_parts = url_parts._replace(path=quote(url_parts.path))
            url = urlunparse(url_parts)
            local_filename, headers = urlretrieve(url, local_filename)
            # todo: check hash value of downloaded file
            # todo: if local_path isn't an existing directory but looks like a directory name
            #       rather than a filename, create that directory and save a file called self.name
            #       within it
            return local_filename
