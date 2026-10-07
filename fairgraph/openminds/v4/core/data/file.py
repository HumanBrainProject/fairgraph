"""
Structured information on a file instance that is accessible via a URL.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import File as OMFile
from fairgraph import KGObject

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
from openminds import IRI


class File(KGObject, OMFile):
    """
    Structured information on a file instance that is accessible via a URL.
    """

    type_ = "https://openminds.om-i.org/types/File"
    default_space = "files"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.v4.core.BehavioralProtocol",
                "openminds.v4.core.Protocol",
                "openminds.v4.ephys.ElectrodeArrayUsage",
                "openminds.v4.ephys.ElectrodeUsage",
                "openminds.v4.ephys.PipetteUsage",
                "openminds.v4.specimen_prep.SlicingDeviceUsage",
            ],
            ["describedIn", "metadataLocation"],
            reverse=["described_in", "metadata_locations"],
            multiple=True,
            description="reverse of described_in, metadata_locations",
        ),
        Property(
            "fully_documents",
            [
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebServiceVersion",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "fullDocumentation",
            reverse="full_documentation",
            multiple=True,
            description="reverse of 'full_documentation'",
        ),
        Property(
            "has_copies",
            "openminds.v4.computation.LocalFile",
            "copyOf",
            reverse="copy_of",
            multiple=True,
            description="reverse of 'copy_of'",
        ),
        Property(
            "is_also_part_of",
            "openminds.v4.computation.WorkflowRecipeVersion",
            "hasPart",
            reverse="has_parts",
            multiple=True,
            description="reverse of 'has_parts'",
        ),
        Property(
            "is_configuration_of",
            "openminds.v4.computation.WorkflowExecution",
            "configuration",
            reverse="configuration",
            multiple=True,
            description="reverse of 'configuration'",
        ),
        Property(
            "is_default_image_for",
            "openminds.v4.sands.CustomCoordinateSpace",
            "defaultImage",
            reverse="default_images",
            multiple=True,
            description="reverse of 'default_images'",
        ),
        Property(
            "is_input_to",
            "openminds.v4.core.DatasetVersion",
            "inputData",
            reverse="input_data",
            multiple=True,
            description="reverse of 'input_data'",
        ),
        Property(
            "is_location_of",
            ["openminds.v4.ephys.Recording", "openminds.v4.sands.ParcellationTerminologyVersion"],
            "dataLocation",
            reverse="data_location",
            multiple=True,
            description="reverse of 'data_location'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.v4.computation.DataAnalysis",
                "openminds.v4.computation.DataCopy",
                "openminds.v4.computation.GenericComputation",
                "openminds.v4.computation.ModelValidation",
                "openminds.v4.computation.Optimization",
                "openminds.v4.computation.Simulation",
                "openminds.v4.computation.Visualization",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.ProtocolExecution",
                "openminds.v4.ephys.RecordingActivity",
                "openminds.v4.stimulation.StimulationActivity",
            ],
            ["output", "outputData"],
            reverse=["output_data", "outputs"],
            multiple=True,
            description="reverse of output_data, outputs",
        ),
        Property(
            "is_preview_of",
            "openminds.v4.core.ServiceLink",
            "previewImage",
            reverse="preview_image",
            multiple=True,
            description="reverse of 'preview_image'",
        ),
        Property(
            "is_reference_for",
            "openminds.v4.computation.ValidationTestVersion",
            "referenceData",
            reverse="reference_data",
            multiple=True,
            description="reverse of 'reference_data'",
        ),
        Property(
            "is_source_data_of",
            "openminds.v4.core.FileArchive",
            "sourceData",
            reverse="source_data",
            multiple=True,
            description="reverse of 'source_data'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v4.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
        Property(
            "specifies",
            [
                "openminds.v4.sands.AtlasAnnotation",
                "openminds.v4.sands.CustomAnnotation",
                "openminds.v4.stimulation.EphysStimulus",
            ],
            "specification",
            reverse="specification",
            multiple=True,
            description="reverse of 'specification'",
        ),
    ]
    aliases = {"hash": "hashes"}
    existence_query_properties = ("iri", "hashes")
    sort_property = "name"

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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
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
            format=ContentType(name=mimetypes.guess_type(relative_path)[0]),
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
