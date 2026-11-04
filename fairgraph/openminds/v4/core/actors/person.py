"""
Structured information on a person.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Person as OMPerson
from fairgraph import KGObject

from fairgraph.queries import Regex
from fairgraph.utility.name_matching import (
    build_given_name_regex,
    build_normalized_regex,
    given_names_compatible,
    names_equivalent,
    split_given_names,
)


class Person(KGObject, OMPerson):
    """
    Structured information on a person.
    """

    type_ = "https://openminds.om-i.org/types/Person"
    default_space = "common"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "activities",
            [
                "openminds.v4.core.ProtocolExecution",
                "openminds.v4.ephys.CellPatching",
                "openminds.v4.ephys.ElectrodePlacement",
                "openminds.v4.ephys.RecordingActivity",
                "openminds.v4.specimen_prep.CranialWindowPreparation",
                "openminds.v4.specimen_prep.TissueCulturePreparation",
                "openminds.v4.specimen_prep.TissueSampleSlicing",
                "openminds.v4.stimulation.StimulationActivity",
            ],
            "performedBy",
            reverse="performed_by",
            multiple=True,
            description="reverse of 'performed_by'",
        ),
        Property(
            "comments",
            "openminds.v4.core.Comment",
            "commenter",
            reverse="commenter",
            multiple=True,
            description="reverse of 'commenter'",
        ),
        Property(
            "coordinated_projects",
            "openminds.v4.core.Project",
            "coordinator",
            reverse="coordinators",
            multiple=True,
            description="reverse of 'coordinators'",
        ),
        Property(
            "developed",
            [
                "openminds.v4.computation.ValidationTest",
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipe",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.MetaDataModel",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.Model",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.Software",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebService",
                "openminds.v4.core.WebServiceVersion",
            ],
            "developer",
            reverse="developers",
            multiple=True,
            description="reverse of 'developers'",
        ),
        Property(
            "funded",
            "openminds.v4.core.Funding",
            "funder",
            reverse="funder",
            multiple=True,
            description="reverse of 'funder'",
        ),
        Property(
            "is_custodian_of",
            [
                "openminds.v4.core.Dataset",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.publications.LivePaper",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.sands.BrainAtlas",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpace",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "custodian",
            reverse="custodians",
            multiple=True,
            description="reverse of 'custodians'",
        ),
        Property(
            "is_owner_of",
            [
                "openminds.v4.ephys.Electrode",
                "openminds.v4.ephys.ElectrodeArray",
                "openminds.v4.ephys.Pipette",
                "openminds.v4.specimen_prep.SlicingDevice",
            ],
            "owner",
            reverse="owners",
            multiple=True,
            description="reverse of 'owners'",
        ),
        Property(
            "is_provider_of",
            "openminds.v4.chemicals.ProductSource",
            "provider",
            reverse="provider",
            multiple=True,
            description="reverse of 'provider'",
        ),
        Property(
            "manufactured",
            "openminds.v4.core.Setup",
            "manufacturer",
            reverse="manufacturers",
            multiple=True,
            description="reverse of 'manufacturers'",
        ),
        Property(
            "published",
            [
                "openminds.v4.publications.Book",
                "openminds.v4.publications.Chapter",
                "openminds.v4.publications.LearningResource",
                "openminds.v4.publications.ScholarlyArticle",
            ],
            "publisher",
            reverse="publisher",
            multiple=True,
            description="reverse of 'publisher'",
        ),
        Property(
            "started",
            [
                "openminds.v4.computation.DataAnalysis",
                "openminds.v4.computation.DataCopy",
                "openminds.v4.computation.GenericComputation",
                "openminds.v4.computation.ModelValidation",
                "openminds.v4.computation.Optimization",
                "openminds.v4.computation.Simulation",
                "openminds.v4.computation.Visualization",
                "openminds.v4.computation.WorkflowExecution",
            ],
            "startedBy",
            reverse="started_by",
            multiple=True,
            description="reverse of 'started_by'",
        ),
    ]
    existence_query_properties = ("given_name", "family_name")
    sort_property = "family_name"

    def __init__(
        self,
        activities=None,
        affiliations=None,
        alternate_names=None,
        associated_accounts=None,
        comments=None,
        contact_information=None,
        coordinated_projects=None,
        developed=None,
        digital_identifiers=None,
        family_name=None,
        funded=None,
        given_name=None,
        is_custodian_of=None,
        is_owner_of=None,
        is_provider_of=None,
        manufactured=None,
        published=None,
        started=None,
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
            activities=activities,
            affiliations=affiliations,
            alternate_names=alternate_names,
            associated_accounts=associated_accounts,
            comments=comments,
            contact_information=contact_information,
            coordinated_projects=coordinated_projects,
            developed=developed,
            digital_identifiers=digital_identifiers,
            family_name=family_name,
            funded=funded,
            given_name=given_name,
            is_custodian_of=is_custodian_of,
            is_owner_of=is_owner_of,
            is_provider_of=is_provider_of,
            manufactured=manufactured,
            published=published,
            started=started,
        )

    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}"

    @classmethod
    def me(cls, client, allow_multiple=False, follow_links=None):
        user_info = client.user_info()
        possible_matches = cls.list(
            client,
            release_status="in progress",
            space="common",
            follow_links=follow_links,
            family_name=user_info.family_name,
            given_name=user_info.given_name,
        )
        if len(possible_matches) == 0:
            person = Person(family_name=user_info.family_name, given_name=user_info.given_name)
        elif len(possible_matches) == 1:
            person = possible_matches[0]
        elif allow_multiple:
            person = possible_matches
        else:
            raise Exception("Found multiple matches")
        return person

    def _find_matching_instances(self, client, in_spaces=None, existence_match="equals"):
        # with existence_match="normalized", look for the same ORCID before looking for the same name,
        # and allow for middle names and initials in the given names
        if existence_match == "normalized":
            instances = self._find_by_identifiers(client, ("ORCID",), in_spaces=in_spaces)
            if instances:
                return instances
            if (
                isinstance(self.given_name, str)
                and split_given_names(self.given_name)
                and isinstance(self.family_name, str)
                and self.family_name.strip()
            ):
                return self._find_by_compatible_names(client, in_spaces=in_spaces)
        return super()._find_matching_instances(client, in_spaces=in_spaces, existence_match=existence_match)

    def _find_by_compatible_names(self, client, in_spaces=None):
        """
        Look for people with an equivalent family name (see `names_equivalent()`) and compatible given names
        (see `given_names_compatible()`), so that "James Maxwell", "James C. Maxwell" and "J. Clerk Maxwell"
        are all found from "James Clerk Maxwell".

        If exactly one of them has the same given names (ignoring case), only that one is returned;
        otherwise, if exactly one has equivalent given names, only that one; otherwise all of them.
        """
        query_filter = {
            "given_name": Regex(build_given_name_regex(self.given_name)),
            "family_name": Regex(build_normalized_regex(self.family_name)),
        }
        compatible = []
        equivalent = []
        exact = []
        for instance in self._run_minimal_query(client, query_filter, in_spaces=in_spaces):
            data = client.instance_from_full_uri(instance["@id"], use_cache=True, release_status="any")
            if data is None:
                continue
            stored_values = self.__class__._deserialize_data(data)
            stored_given_name = stored_values.get("given_name", None)
            stored_family_name = stored_values.get("family_name", None)
            if not (isinstance(stored_given_name, str) and isinstance(stored_family_name, str)):
                continue
            if not (
                names_equivalent(stored_family_name, self.family_name)
                and given_names_compatible(stored_given_name, self.given_name)
            ):
                continue
            compatible.append(instance)
            if names_equivalent(stored_given_name, self.given_name):
                equivalent.append(instance)
                if (
                    stored_given_name.lower() == self.given_name.lower()
                    and stored_family_name.lower() == self.family_name.lower()
                ):
                    exact.append(instance)
        for candidates in (exact, equivalent):
            if len(candidates) == 1:
                return candidates
        return compatible

    def _adopt_matched_values(self, data, existence_match):
        super()._adopt_matched_values(data, existence_match)
        # with existence_match="normalized", the given names may differ by more than names_equivalent() allows
        if existence_match == "normalized":
            stored_given_name = self.__class__._deserialize_data(data).get("given_name", None)
            if (
                isinstance(stored_given_name, str)
                and isinstance(self.given_name, str)
                and stored_given_name != self.given_name
                and given_names_compatible(stored_given_name, self.given_name)
            ):
                self.given_name = stored_given_name
