import sys
import inspect
from fairgraph.kgobject import KGObject
from fairgraph.embedded import EmbeddedMetadata

from .action_status_type import ActionStatusType
from .age_category import AgeCategory
from .analysis_technique import AnalysisTechnique
from .anatomical_axes_orientation import AnatomicalAxesOrientation
from .anatomical_identification_type import AnatomicalIdentificationType
from .anatomical_plane import AnatomicalPlane
from .annotation_criteria_type import AnnotationCriteriaType
from .annotation_type import AnnotationType
from .atlas_type import AtlasType
from .auditory_stimulus_type import AuditoryStimulusType
from .biological_order import BiologicalOrder
from .biological_process import BiologicalProcess
from .biological_sex import BiologicalSex
from .breeding_type import BreedingType
from .cell_culture_type import CellCultureType
from .cell_type import CellType
from .chemical_mixture_type import ChemicalMixtureType
from .colormap import Colormap
from .contribution_type import ContributionType
from .cranial_window_construction_type import CranialWindowConstructionType
from .cranial_window_reinforcement_type import CranialWindowReinforcementType
from .criteria_quality_type import CriteriaQualityType
from .data_type import DataType
from .device_type import DeviceType
from .difference_measure import DifferenceMeasure
from .disease import Disease
from .disease_model import DiseaseModel
from .educational_level import EducationalLevel
from .electrical_stimulus_type import ElectricalStimulusType
from .ethics_assessment import EthicsAssessment
from .experimental_approach import ExperimentalApproach
from .file_bundle_grouping import FileBundleGrouping
from .file_repository_type import FileRepositoryType
from .file_usage_role import FileUsageRole
from .genetic_strain_type import GeneticStrainType
from .gustatory_stimulus_type import GustatoryStimulusType
from .handedness import Handedness
from .language import Language
from .laterality import Laterality
from .learning_resource_type import LearningResourceType
from .measured_quantity import MeasuredQuantity
from .measured_signal_type import MeasuredSignalType
from .meta_data_model_type import MetaDataModelType
from .model_abstraction_level import ModelAbstractionLevel
from .model_scope import ModelScope
from .molecular_entity import MolecularEntity
from .mri_pulse_sequence import MRIPulseSequence
from .olfactory_stimulus_type import OlfactoryStimulusType
from .operating_device import OperatingDevice
from .operating_system import OperatingSystem
from .optical_stimulus_type import OpticalStimulusType
from .organ import Organ
from .organism_substance import OrganismSubstance
from .organism_system import OrganismSystem
from .patch_clamp_variation import PatchClampVariation
from .preparation_type import PreparationType
from .product_accessibility import ProductAccessibility
from .programming_language import ProgrammingLanguage
from .qualitative_overlap import QualitativeOverlap
from .semantic_data_type import SemanticDataType
from .service import Service
from .setup_type import SetupType
from .software_application_category import SoftwareApplicationCategory
from .software_feature import SoftwareFeature
from .species import Species
from .stimulation_approach import StimulationApproach
from .stimulation_technique import StimulationTechnique
from .subcellular_entity import SubcellularEntity
from .subject_attribute import SubjectAttribute
from .tactile_stimulus_type import TactileStimulusType
from .technique import Technique
from .term_suggestion import TermSuggestion
from .terminology import Terminology
from .tissue_sample_attribute import TissueSampleAttribute
from .tissue_sample_type import TissueSampleType
from .type_of_uncertainty import TypeOfUncertainty
from .uberon_parcellation import UBERONParcellation
from .unit_of_measurement import UnitOfMeasurement
from .visual_stimulus_type import VisualStimulusType


def list_kg_classes():
    """List all KG classes defined in this module"""
    return [
        obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__.startswith(__name__)
    ]


def list_embedded_metadata_classes():
    """List all embedded metadata classes defined in this module"""
    return [
        obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isclass(obj) and issubclass(obj, EmbeddedMetadata) and obj.__module__.startswith(__name__)
    ]


def set_error_handling(value):
    """
    Control validation for all classes in this module.

    Args:
        value (str): action to follow when there is a validation failure.
            (e.g. if a required property is not provided).
            Possible values: "error", "warning", "log", None
    """
    for cls in list_kg_classes() + list_embedded_metadata_classes():
        cls.set_error_handling(value)
