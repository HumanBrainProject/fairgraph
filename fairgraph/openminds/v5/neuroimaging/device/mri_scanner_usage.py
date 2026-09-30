"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.neuroimaging import MRIScannerUsage as OMMRIScannerUsage
from fairgraph import KGObject


from numbers import Real


class MRIScannerUsage(KGObject, OMMRIScannerUsage):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/MRIScannerUsage"
    default_space = "in-depth"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "generation_device",
            "openminds.v5.stimulation.EphysStimulus",
            "generatedBy",
            reverse="generated_by",
            multiple=True,
            description="reverse of 'generated_by'",
        ),
        Property(
            "is_used_to_obtain",
            [
                "openminds.v5.core.GridImage",
                "openminds.v5.core.GridImageSequence",
                "openminds.v5.core.GridImageStack",
                "openminds.v5.core.GridVolume",
                "openminds.v5.core.GridVolumeSequence",
                "openminds.v5.core.Measurement",
                "openminds.v5.core.RegularTimeSeries",
            ],
            "obtainedWith",
            reverse="obtained_with",
            multiple=True,
            description="reverse of 'obtained_with'",
        ),
        Property(
            "placed_by",
            "openminds.v5.ephys.ElectrodePlacement",
            "device",
            reverse="devices",
            multiple=True,
            description="reverse of 'devices'",
        ),
        Property(
            "used_in",
            [
                "openminds.v5.ephys.CellPatching",
                "openminds.v5.neuroimaging.DynamicMRIAcquisition",
                "openminds.v5.neuroimaging.StaticMRIAcquisition",
            ],
            "device",
            reverse="device",
            multiple=True,
            description="reverse of 'device'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        acceleration_factor=None,
        device=None,
        diffusion_encoding_parameters=None,
        dwell_time=None,
        echo_times=None,
        fat_suppression_technique=None,
        field_of_view=None,
        flip_angle=None,
        generation_device=None,
        gradient_correction=None,
        inversion_time=None,
        is_used_to_obtain=None,
        matrix_sizes=None,
        metadata_locations=None,
        mri_weighting=None,
        mt_pulse_shape=None,
        number_of_discarded_volumes=None,
        number_of_excitations=None,
        number_of_slices=None,
        parallel_acquisition_technique=None,
        phase_encoding_directions=None,
        placed_by=None,
        receiver_bandwidth=None,
        repetition_time=None,
        slice_angulations=None,
        slice_gap=None,
        slice_orientation=None,
        slice_thickness=None,
        slice_timing=None,
        spatial_encoding=None,
        spoiling_technique=None,
        total_read_out_time=None,
        transmitter_bandwidth=None,
        used_coils=None,
        used_in=None,
        used_specimen=None,
        voxel_size=None,
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
            lookup_label=lookup_label,
            acceleration_factor=acceleration_factor,
            device=device,
            diffusion_encoding_parameters=diffusion_encoding_parameters,
            dwell_time=dwell_time,
            echo_times=echo_times,
            fat_suppression_technique=fat_suppression_technique,
            field_of_view=field_of_view,
            flip_angle=flip_angle,
            generation_device=generation_device,
            gradient_correction=gradient_correction,
            inversion_time=inversion_time,
            is_used_to_obtain=is_used_to_obtain,
            matrix_sizes=matrix_sizes,
            metadata_locations=metadata_locations,
            mri_weighting=mri_weighting,
            mt_pulse_shape=mt_pulse_shape,
            number_of_discarded_volumes=number_of_discarded_volumes,
            number_of_excitations=number_of_excitations,
            number_of_slices=number_of_slices,
            parallel_acquisition_technique=parallel_acquisition_technique,
            phase_encoding_directions=phase_encoding_directions,
            placed_by=placed_by,
            receiver_bandwidth=receiver_bandwidth,
            repetition_time=repetition_time,
            slice_angulations=slice_angulations,
            slice_gap=slice_gap,
            slice_orientation=slice_orientation,
            slice_thickness=slice_thickness,
            slice_timing=slice_timing,
            spatial_encoding=spatial_encoding,
            spoiling_technique=spoiling_technique,
            total_read_out_time=total_read_out_time,
            transmitter_bandwidth=transmitter_bandwidth,
            used_coils=used_coils,
            used_in=used_in,
            used_specimen=used_specimen,
            voxel_size=voxel_size,
        )
