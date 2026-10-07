"""
Structured information on a file instance that is accessible via a URL.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import File as OMFile
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
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.v5.core.BehavioralProtocol",
                "openminds.v5.core.Protocol",
                "openminds.v5.ephys.ElectrodeArrayUsage",
                "openminds.v5.ephys.ElectrodeUsage",
                "openminds.v5.ephys.PipetteUsage",
                "openminds.v5.neuroimaging.MRICoilUsage",
                "openminds.v5.neuroimaging.MRIScannerUsage",
                "openminds.v5.specimen_prep.SlicingDeviceUsage",
            ],
            ["describedIn", "metadataLocation"],
            reverse=["described_in", "metadata_locations"],
            multiple=True,
            description="reverse of described_in, metadata_locations",
        ),
        Property(
            "documents",
            [
                "openminds.v5.computation.ValidationTest",
                "openminds.v5.computation.WorkflowRecipe",
                "openminds.v5.core.Dataset",
                "openminds.v5.core.Interface",
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.Service",
                "openminds.v5.core.Software",
                "openminds.v5.core.SoftwareVersion",
                "openminds.v5.publications.LivePaper",
                "openminds.v5.publications.LivePaperVersion",
                "openminds.v5.sands.AnatomicalAtlas",
                "openminds.v5.sands.AnatomicalAtlasVersion",
                "openminds.v5.sands.CommonCoordinateFramework",
                "openminds.v5.sands.CommonCoordinateFrameworkVersion",
            ],
            "documentation",
            reverse="documentation",
            multiple=True,
            description="reverse of 'documentation'",
        ),
        Property(
            "has_copies",
            "openminds.v5.core.LocalFile",
            "copyOf",
            reverse="copy_of",
            multiple=True,
            description="reverse of 'copy_of'",
        ),
        Property(
            "is_also_part_of",
            "openminds.v5.computation.WorkflowRecipeVersion",
            "hasPart",
            reverse="has_parts",
            multiple=True,
            description="reverse of 'has_parts'",
        ),
        Property(
            "is_configuration_of",
            "openminds.v5.computation.WorkflowExecution",
            "configuration",
            reverse="configuration",
            multiple=True,
            description="reverse of 'configuration'",
        ),
        Property(
            "is_default_image_for",
            "openminds.v5.sands.CustomCoordinateFramework",
            "defaultImage",
            reverse="default_images",
            multiple=True,
            description="reverse of 'default_images'",
        ),
        Property(
            "is_input_to",
            "openminds.v5.core.DatasetVersion",
            "inputData",
            reverse="input_data",
            multiple=True,
            description="reverse of 'input_data'",
        ),
        Property(
            "is_location_of",
            [
                "openminds.v5.core.GridImage",
                "openminds.v5.core.GridImageSequence",
                "openminds.v5.core.GridImageStack",
                "openminds.v5.core.GridVolume",
                "openminds.v5.core.GridVolumeSequence",
                "openminds.v5.core.RegularTimeSeries",
            ],
            "dataLocation",
            reverse="data_location",
            multiple=True,
            description="reverse of 'data_location'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.ephys.RecordingActivity",
                "openminds.v5.stimulation.StimulationActivity",
            ],
            ["output", "outputData"],
            reverse=["output_data", "outputs"],
            multiple=True,
            description="reverse of output_data, outputs",
        ),
        Property(
            "is_preview_of",
            "openminds.v5.core.ServiceLink",
            "previewImage",
            reverse="preview_image",
            multiple=True,
            description="reverse of 'preview_image'",
        ),
        Property(
            "is_reference_for",
            "openminds.v5.computation.ValidationTestVersion",
            "referenceData",
            reverse="reference_data",
            multiple=True,
            description="reverse of 'reference_data'",
        ),
        Property(
            "is_source_data_of",
            "openminds.v5.core.FileArchive",
            "sourceData",
            reverse="source_data",
            multiple=True,
            description="reverse of 'source_data'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v5.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
        Property(
            "specifies",
            [
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.sands.AtlasAnnotation",
                "openminds.v5.sands.CustomAnnotation",
                "openminds.v5.stimulation.EphysStimulus",
            ],
            "specification",
            reverse="specification",
            multiple=True,
            description="reverse of 'specification'",
        ),
        Property(
            "used_in",
            ["openminds.v5.neuroimaging.DynamicMRIAcquisition", "openminds.v5.neuroimaging.StaticMRIAcquisition"],
            "registrationData",
            reverse="registration_data",
            multiple=True,
            description="reverse of 'registration_data'",
        ),
    ]
    aliases = {"hash": "hashes"}
    existence_query_properties = ("iri", "hashes")

    def __init__(
        self,
        name=None,
        content_description=None,
        data_types=None,
        describes=None,
        documents=None,
        file_repository=None,
        format=None,
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
        used_in=None,
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
            documents=documents,
            file_repository=file_repository,
            format=format,
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
            used_in=used_in,
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
