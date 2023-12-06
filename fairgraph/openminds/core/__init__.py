import sys
import inspect
from fairgraph.kgobject import KGObject
from fairgraph.embedded import EmbeddedMetadata

from .research import (
    ProtocolExecution,
    SubjectGroup,
    Subject,
    Strain,
    TissueSampleCollection,
    BehavioralProtocol,
    StringProperty,
    CustomPropertySet,
    TissueSampleState,
    SubjectState,
    TissueSample,
    Protocol,
    TissueSampleCollectionState,
    Configuration,
    NumericalProperty,
    SubjectGroupState,
    PropertyValueList,
)
from .products import (
    Dataset,
    Project,
    DatasetVersion,
    SoftwareVersion,
    MetaDataModelVersion,
    Model,
    Software,
    Setup,
    WebServiceVersion,
    MetaDataModel,
    WebService,
    ModelVersion,
)
from .digital_identifier import (
    ISSN,
    IdentifiersDotOrgID,
    DOI,
    RORID,
    RRID,
    ORCID,
    GRIDID,
    ISBN,
    StockNumber,
    HANDLE,
    SWHID,
)
from .miscellaneous import (
    QuantitativeValue,
    Funding,
    ResearchProductGroup,
    WebResource,
    QuantitativeValueRange,
    QuantitativeValueArray,
    Comment,
)
from .actors import Contribution, AccountInformation, Consortium, Affiliation, Organization, ContactInformation, Person
from .data import (
    ServiceLink,
    ContentTypePattern,
    Copyright,
    FileArchive,
    Hash,
    ContentType,
    FilePathPattern,
    FileRepository,
    License,
    File,
    FileBundle,
    FileRepositoryStructure,
    Measurement,
)


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
            (e.g. if a required field is not provided).
            Possible values: "error", "warning", "log", None
    """
    for cls in list_kg_classes() + list_embedded_metadata_classes():
        cls.set_error_handling(value)
