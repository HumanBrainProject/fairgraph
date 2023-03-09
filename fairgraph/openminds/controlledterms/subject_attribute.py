"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - treated
         - A subject that is in a permanently or temporarily altered state compared to its natural state following some kind of treatment.
       * - alive
         - An organism that is not dead.
       * - drugged
         - A temporary state of an organism in which it is under the influence of a sedative, narcotic or any other typye of drug.
       * - has inserted device
         - A typically temporary state of an organism during which a device (e.g., an electrode) is inserted to measure or stimulate bodily functions.
       * - head restrained
         - An organism that has been restrained on the head causing e.g., decreased motion range and/or increased resistance in movement.
       * - awake
         - A temporary state of an organism in which it is fully alert and aware.
       * - freely moving
         - An organism that can move easily, without any obstacles or resistance.
       * - has implanted device
         - A typically chronic state of an organism after surgical implantation of a device (e.g., an electrode, a pacemaker) to measure or stimulate bodily functions.
       * - restrained
         - An organism that has been restrained in any way causing e.g., decreased motion range and/or increased resistance in movement.
       * - postoperative
         - A temporary state of an organism in the time period that immediately follows a surgical procedure.
       * - control
         - An organism that is part of a study and does not receive the treatment being tested.
       * - deceased
         - An organism that is no longer living.
       * - anaesthetized
         - A temporary state of an organism induced by anaestetic substances that cause the reduction or loss of pain sensation with or without loss of consciousness.
       * - knockin
         - An organism that underwent a targeted insertation of foreign genetic material in the existing genetic material (i.e. a gene).
       * - preoperative
         - A temporary state of an organism in the time period between the decision to have surgery and the beginning of the surgical procedure.
       * - knockout
         - An organism that underwent a targeted excision or silencing/inactivation of existing genetic material (i.e. a gene).
       * - alert
         - A temporary state of an organism in which it can quickly perceive and act.
       * - asleep
         - A periodic, readily reversible state of an organism with reduced awareness and typically lower metabolic activity.
       * - comatose
         - A deep state of prolonged unconsciousness in which the organism cannot be awakened (temporarily or terminally), is unresponsive and typically displays depressed cerebral activity.
       * - untreated
         - A subject in its natural state which has not been exposed to any kind of state-altering treatment.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base import KGObject, IRI
from fairgraph.fields import Field




class SubjectAttribute(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - treated
         - A subject that is in a permanently or temporarily altered state compared to its natural state following some kind of treatment.
       * - alive
         - An organism that is not dead.
       * - drugged
         - A temporary state of an organism in which it is under the influence of a sedative, narcotic or any other typye of drug.
       * - has inserted device
         - A typically temporary state of an organism during which a device (e.g., an electrode) is inserted to measure or stimulate bodily functions.
       * - head restrained
         - An organism that has been restrained on the head causing e.g., decreased motion range and/or increased resistance in movement.
       * - awake
         - A temporary state of an organism in which it is fully alert and aware.
       * - freely moving
         - An organism that can move easily, without any obstacles or resistance.
       * - has implanted device
         - A typically chronic state of an organism after surgical implantation of a device (e.g., an electrode, a pacemaker) to measure or stimulate bodily functions.
       * - restrained
         - An organism that has been restrained in any way causing e.g., decreased motion range and/or increased resistance in movement.
       * - postoperative
         - A temporary state of an organism in the time period that immediately follows a surgical procedure.
       * - control
         - An organism that is part of a study and does not receive the treatment being tested.
       * - deceased
         - An organism that is no longer living.
       * - anaesthetized
         - A temporary state of an organism induced by anaestetic substances that cause the reduction or loss of pain sensation with or without loss of consciousness.
       * - knockin
         - An organism that underwent a targeted insertation of foreign genetic material in the existing genetic material (i.e. a gene).
       * - preoperative
         - A temporary state of an organism in the time period between the decision to have surgery and the beginning of the surgical procedure.
       * - knockout
         - An organism that underwent a targeted excision or silencing/inactivation of existing genetic material (i.e. a gene).
       * - alert
         - A temporary state of an organism in which it can quickly perceive and act.
       * - asleep
         - A periodic, readily reversible state of an organism with reduced awareness and typically lower metabolic activity.
       * - comatose
         - A deep state of prolonged unconsciousness in which the organism cannot be awakened (temporarily or terminally), is unresponsive and typically displays depressed cerebral activity.
       * - untreated
         - A subject in its natural state which has not been exposed to any kind of state-altering treatment.

    """
    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/SubjectAttribute"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the subject attribute."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the subject attribute."),
        Field("interlex_identifier", IRI, "vocab:interlexIdentifier", multiple=False, required=False,
              doc="Persistent identifier for a term registered in the InterLex project."),
        Field("knowledge_space_link", IRI, "vocab:knowledgeSpaceLink", multiple=False, required=False,
              doc="Persistent link to an encyclopedia entry in the Knowledge Space project."),
        Field("preferred_ontology_identifier", IRI, "vocab:preferredOntologyIdentifier", multiple=False, required=False,
              doc="Persistent identifier of a preferred ontological term."),
        Field("synonyms", str, "vocab:synonym", multiple=True, required=False,
              doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses."),

    ]
    existence_query_fields = ('name',)
