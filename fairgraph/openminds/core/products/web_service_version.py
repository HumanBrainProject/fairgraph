"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property

from fairgraph.errors import ResolutionFailure
from .web_service import WebService
from datetime import date
from fairgraph.base import IRI


class WebServiceVersion(KGObject):
    """
    <description not available>
    """

    default_space = "webservice"
    type_ = ["https://openminds.ebrains.eu/core/WebServiceVersion"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "accessibility",
            "openminds.controlled_terms.ProductAccessibility",
            "vocab:accessibility",
            required=True,
            doc="Level to which something is accessible to the web service version.",
        ),
        Property(
            "copyright",
            "openminds.core.Copyright",
            "vocab:copyright",
            doc="Exclusive and assignable legal right of an originator to reproduce, publish, sell, or distribute the matter and form of a creative work for a defined time period.",
        ),
        Property(
            "custodians",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:custodian",
            multiple=True,
            doc="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product.",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the web service version.",
        ),
        Property(
            "developers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:developer",
            multiple=True,
            doc="Legal person that creates or improves products or services (e.g., software, applications, etc.).",
        ),
        Property(
            "full_documentation",
            ["openminds.core.DOI", "openminds.core.File", "openminds.core.WebResource"],
            "vocab:fullDocumentation",
            required=True,
            doc="Non-abridged instructions, comments, and information for using a particular product.",
        ),
        Property("full_name", str, "vocab:fullName", doc="Whole, non-abbreviated name of the web service version."),
        Property(
            "funding",
            "openminds.core.Funding",
            "vocab:funding",
            multiple=True,
            doc="Money provided by a legal person for a particular purpose.",
        ),
        Property(
            "has_parts",
            "openminds.core.SoftwareVersion",
            "vocab:hasPart",
            multiple=True,
            doc="no description available",
        ),
        Property("homepage", IRI, "vocab:homepage", doc="Main website of the web service version."),
        Property(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
        Property(
            "input_formats",
            "openminds.core.ContentType",
            "vocab:inputFormat",
            multiple=True,
            doc="Format of data that is put into a process or machine.",
        ),
        Property(
            "is_alternative_version_of",
            "openminds.core.WebServiceVersion",
            "vocab:isAlternativeVersionOf",
            multiple=True,
            doc="Reference to an original form where the essence was preserved, but presented in an alternative form.",
        ),
        Property(
            "is_new_version_of",
            "openminds.core.WebServiceVersion",
            "vocab:isNewVersionOf",
            doc="Reference to a previous (potentially outdated) particular form of something.",
        ),
        Property(
            "keywords",
            [
                "openminds.controlled_terms.ActionStatusType",
                "openminds.controlled_terms.AgeCategory",
                "openminds.controlled_terms.AnalysisTechnique",
                "openminds.controlled_terms.AnatomicalAxesOrientation",
                "openminds.controlled_terms.AnatomicalIdentificationType",
                "openminds.controlled_terms.AnatomicalPlane",
                "openminds.controlled_terms.AnnotationCriteriaType",
                "openminds.controlled_terms.AnnotationType",
                "openminds.controlled_terms.AtlasType",
                "openminds.controlled_terms.AuditoryStimulusType",
                "openminds.controlled_terms.BiologicalOrder",
                "openminds.controlled_terms.BiologicalProcess",
                "openminds.controlled_terms.BiologicalSex",
                "openminds.controlled_terms.BreedingType",
                "openminds.controlled_terms.CellCultureType",
                "openminds.controlled_terms.CellType",
                "openminds.controlled_terms.ChemicalMixtureType",
                "openminds.controlled_terms.Colormap",
                "openminds.controlled_terms.ContributionType",
                "openminds.controlled_terms.CranialWindowConstructionType",
                "openminds.controlled_terms.CranialWindowReinforcementType",
                "openminds.controlled_terms.CriteriaQualityType",
                "openminds.controlled_terms.DataType",
                "openminds.controlled_terms.DeviceType",
                "openminds.controlled_terms.DifferenceMeasure",
                "openminds.controlled_terms.Disease",
                "openminds.controlled_terms.DiseaseModel",
                "openminds.controlled_terms.EducationalLevel",
                "openminds.controlled_terms.ElectricalStimulusType",
                "openminds.controlled_terms.EthicsAssessment",
                "openminds.controlled_terms.ExperimentalApproach",
                "openminds.controlled_terms.FileBundleGrouping",
                "openminds.controlled_terms.FileRepositoryType",
                "openminds.controlled_terms.FileUsageRole",
                "openminds.controlled_terms.GeneticStrainType",
                "openminds.controlled_terms.GustatoryStimulusType",
                "openminds.controlled_terms.Handedness",
                "openminds.controlled_terms.Language",
                "openminds.controlled_terms.Laterality",
                "openminds.controlled_terms.LearningResourceType",
                "openminds.controlled_terms.MeasuredQuantity",
                "openminds.controlled_terms.MeasuredSignalType",
                "openminds.controlled_terms.MetaDataModelType",
                "openminds.controlled_terms.ModelAbstractionLevel",
                "openminds.controlled_terms.ModelScope",
                "openminds.controlled_terms.MolecularEntity",
                "openminds.controlled_terms.OlfactoryStimulusType",
                "openminds.controlled_terms.OperatingDevice",
                "openminds.controlled_terms.OperatingSystem",
                "openminds.controlled_terms.OpticalStimulusType",
                "openminds.controlled_terms.Organ",
                "openminds.controlled_terms.OrganismSubstance",
                "openminds.controlled_terms.OrganismSystem",
                "openminds.controlled_terms.PatchClampVariation",
                "openminds.controlled_terms.PreparationType",
                "openminds.controlled_terms.ProductAccessibility",
                "openminds.controlled_terms.ProgrammingLanguage",
                "openminds.controlled_terms.QualitativeOverlap",
                "openminds.controlled_terms.SemanticDataType",
                "openminds.controlled_terms.Service",
                "openminds.controlled_terms.SetupType",
                "openminds.controlled_terms.SoftwareApplicationCategory",
                "openminds.controlled_terms.SoftwareFeature",
                "openminds.controlled_terms.Species",
                "openminds.controlled_terms.StimulationApproach",
                "openminds.controlled_terms.StimulationTechnique",
                "openminds.controlled_terms.SubcellularEntity",
                "openminds.controlled_terms.SubjectAttribute",
                "openminds.controlled_terms.TactileStimulusType",
                "openminds.controlled_terms.Technique",
                "openminds.controlled_terms.TermSuggestion",
                "openminds.controlled_terms.Terminology",
                "openminds.controlled_terms.TissueSampleAttribute",
                "openminds.controlled_terms.TissueSampleType",
                "openminds.controlled_terms.TypeOfUncertainty",
                "openminds.controlled_terms.UBERONParcellation",
                "openminds.controlled_terms.UnitOfMeasurement",
                "openminds.controlled_terms.VisualStimulusType",
            ],
            "vocab:keyword",
            multiple=True,
            doc="Significant word or concept that are representative of the web service version.",
        ),
        Property(
            "other_contributions",
            "openminds.core.Contribution",
            "vocab:otherContribution",
            multiple=True,
            doc="Giving or supplying of something (such as money or time) as a part or share other than what is covered elsewhere.",
        ),
        Property(
            "output_formats",
            "openminds.core.ContentType",
            "vocab:outputFormat",
            multiple=True,
            doc="Format of data that comes out of, is delivered or produced by a process or machine.",
        ),
        Property(
            "related_publications",
            [
                "openminds.core.DOI",
                "openminds.core.HANDLE",
                "openminds.core.ISBN",
                "openminds.core.ISSN",
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.ScholarlyArticle",
            ],
            "vocab:relatedPublication",
            multiple=True,
            doc="Reference to something that was made available for the general public to see or buy.",
        ),
        Property(
            "release_date",
            date,
            "vocab:releaseDate",
            required=True,
            doc="Fixed date on which a product is due to become or was made available for the general public to see or buy",
        ),
        Property(
            "repository",
            "openminds.core.FileRepository",
            "vocab:repository",
            doc="Place, room, or container where something is deposited or stored.",
        ),
        Property(
            "short_name",
            str,
            "vocab:shortName",
            required=True,
            doc="Shortened or fully abbreviated name of the web service version.",
        ),
        Property(
            "support_channels",
            str,
            "vocab:supportChannel",
            multiple=True,
            doc="Way of communication used to interact with users or customers.",
        ),
        Property(
            "version_identifier",
            str,
            "vocab:versionIdentifier",
            required=True,
            doc="Term or code used to identify the version of something.",
        ),
        Property(
            "version_innovation",
            str,
            "vocab:versionInnovation",
            required=True,
            doc="Documentation on what changed in comparison to a previously published form of something.",
        ),
        Property(
            "comments",
            "openminds.core.Comment",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
        Property(
            "is_old_version_of",
            "openminds.core.WebServiceVersion",
            "^vocab:isNewVersionOf",
            reverse="is_new_version_of",
            multiple=True,
            doc="reverse of 'isNewVersionOf'",
        ),
        Property(
            "is_part_of",
            ["openminds.core.Project", "openminds.core.ResearchProductGroup"],
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Property(
            "is_version_of",
            "openminds.core.WebService",
            "^vocab:hasVersion",
            reverse="has_versions",
            multiple=True,
            doc="reverse of 'hasVersion'",
        ),
        Property(
            "learning_resources",
            "openminds.publications.LearningResource",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
        Property(
            "used_for",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
            ],
            "^vocab:environment",
            reverse="environments",
            multiple=True,
            doc="reverse of 'environment'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("short_name", "version_identifier")

    def __init__(
        self,
        name=None,
        alias=None,
        accessibility=None,
        comments=None,
        copyright=None,
        custodians=None,
        description=None,
        developers=None,
        full_documentation=None,
        full_name=None,
        funding=None,
        has_parts=None,
        homepage=None,
        how_to_cite=None,
        input_formats=None,
        is_alternative_version_of=None,
        is_new_version_of=None,
        is_old_version_of=None,
        is_part_of=None,
        is_version_of=None,
        keywords=None,
        learning_resources=None,
        other_contributions=None,
        output_formats=None,
        related_publications=None,
        release_date=None,
        repository=None,
        short_name=None,
        support_channels=None,
        used_for=None,
        version_identifier=None,
        version_innovation=None,
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
            alias=alias,
            accessibility=accessibility,
            comments=comments,
            copyright=copyright,
            custodians=custodians,
            description=description,
            developers=developers,
            full_documentation=full_documentation,
            full_name=full_name,
            funding=funding,
            has_parts=has_parts,
            homepage=homepage,
            how_to_cite=how_to_cite,
            input_formats=input_formats,
            is_alternative_version_of=is_alternative_version_of,
            is_new_version_of=is_new_version_of,
            is_old_version_of=is_old_version_of,
            is_part_of=is_part_of,
            is_version_of=is_version_of,
            keywords=keywords,
            learning_resources=learning_resources,
            other_contributions=other_contributions,
            output_formats=output_formats,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            short_name=short_name,
            support_channels=support_channels,
            used_for=used_for,
            version_identifier=version_identifier,
            version_innovation=version_innovation,
        )

    def is_version_of(self, client):
        parents = WebService.list(client, scope=self.scope, space=self.space, versions=self)
        if len(parents) == 0:
            raise ResolutionFailure("Unable to find parent")
        else:
            assert len(parents) == 1
            return parents[0]
