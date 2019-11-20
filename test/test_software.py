# encoding: utf-8
"""
Tests of the "software" module
"""

from datetime import date
import json
from fairgraph.software import Software, OperatingSystem, SoftwareCategory, ProgrammingLanguage, License
from fairgraph.core import Person, Organization
from fairgraph.commons import License


class MockInstance(object):

    def __init__(self, data):
        self.data = data


class TestSoftware(object):

    def test__build_data(self):

        input_data = dict(
            name="PyNN v0.9.4",
            version="0.9.4",
            summary="A Python package for simulator-independent specification of neuronal network models",
            description="PyNN (pronounced 'pine') is a simulator-independent language for building neuronal network models.",
            #identifier=Identifier("RRID:SCR_002715"),
            citation=("Davison AP, Brüderle D, Eppler JM, Kremkow J, Muller E, Pecevski DA, Perrinet L and Yger P (2009) "
                      "PyNN: a common interface for neuronal network simulators. "
                      "Front. Neuroinform. 2:11 doi:10.3389/neuro.11.011.2008"),
            license=License("CeCILL v2"),
            release_date=date(2019, 3, 22),
            previous_version=None,
            authors=[Person("Davison", "Andrew", "andrew.davison@unic.cnrs-gif.fr")],
            project=None,
            image="https://neuralensemble.org/static/photos/pynn_logo.png",
            #download_url="https://files.pythonhosted.org/packages/a2/1c/78b5d476900254c2c638a29a343ea12985ea16b12c7aed8cec252215c848/PyNN-0.9.4.tar.gz",
            #access_url="https://pypi.org/project/PyNN/0.9.4/",
            categories=None,
            subcategories=None,
            operating_system=[OperatingSystem("Linux"), OperatingSystem("MacOS"), OperatingSystem("Windows")],
            release_notes="http://neuralensemble.org/docs/PyNN/releases/0.9.4.html",
            requirements="neo, lazyarray",
            copyright=Organization("The PyNN community"),
            components=None,
            part_of=None,
            funding=[Organization("CNRS"), Organization("Human Brain Project")],
            programming_language=ProgrammingLanguage("Python"),
            features=None,
            keywords="simulation, neuroscience",
            is_free=True,
            homepage="https://neuralensemble.org/PyNN/",
            documentation="http://neuralensemble.org/docs/PyNN/",
            help="https://groups.google.com/forum/#!forum/neuralensemble"
        )
        software_release = Software(**input_data)
        kg_data = software_release._build_data(client=None)
        assert kg_data == {
            'schema:name': input_data["name"],
            'schema:version': input_data["version"],
            'schema:headline': input_data["summary"],
            'schema:description': input_data["description"],
            'schema:citation': input_data["citation"],
            'schema:license': {'@id': input_data["license"].iri, 'label': input_data["license"].label},
            'schema:dateCreated': '2019-03-22',
            'schema:copyrightYear': input_data["release_date"].year,
            # 'prov:wasAttributedTo': [
            #     {'@id': None, '@type': ['nsg:Person', 'prov:Agent']}
            # ],
            'schema:author': {'@id': None, '@type': ['nsg:Person', 'prov:Agent']},
            'schema:image': {'@id': input_data["image"]},
            # 'schema:distribution': {
            #     'schema:downloadURL': {"@id": input_data["download_url"]},
            #     'schema:accessURL': {"@id": input_data["access_url"]}
            # },
            'schema:operatingSystem': [
                {'@id': os.iri, 'label': os.label}
                for os in input_data["operating_system"]
            ],
            'schema:releaseNotes': input_data["release_notes"],
            #'schema:softwareRequirements': input_data["requirements"],
            'schema:requirements': input_data["requirements"],
            'schema:copyrightHolder': {'@id': None, '@type': 'nsg:Organization'},
            'schema:funder': [{'@id': None, '@type': 'nsg:Organization'}, {'@id': None, '@type': 'nsg:Organization'}],
            'schema:programmingLanguage': {'@id': input_data["programming_language"].iri, 'label': input_data["programming_language"].label},
            'schema:keywords': input_data["keywords"],
            'schema:isAccessibleForFree': input_data["is_free"],
            'schema:url': {'@id': input_data["homepage"]},
            'schema:documentation': {'@id': input_data["documentation"]},
            #'schema:softwareHelp': {'@id': input_data["help"]}
            'schema:help': {'@id': input_data["help"]}
        }

    def test_from_instance(self):
        instance_data = json.loads("""{
            "@context": [
                "https://nexus-int.humanbrainproject.org/v0/contexts/neurosciencegraph/core/data/v0.1.0",
                {
                    "dbpedia": "http://dbpedia.org/resource/",
                    "wd": "http://www.wikidata.org/entity/",
                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                    "label": "rdfs:label"
                },
                "https://nexus-int.humanbrainproject.org/v0/contexts/nexus/core/resource/v0.3.0"
            ],
            "@id": "https://nexus-int.humanbrainproject.org/v0/data/softwarecatalog/software/software/v0.1.1/beb9546e-c801-4159-ab3f-5678a5f75f33",
            "@type": [
                "nsg:Software",
                "nsg:Entity"
            ],
            "nsg:providerId": "doi:10.5281/zenodo.1400175",
            "schema:applicationCategory": [
                {
                    "@id": "https://www.wikidata.org/wiki/Q166142",
                    "label": "application"
                }
            ],
            "schema:applicationSubCategory": [
                {
                    "@id": "https://www.wikidata.org/wiki/Q184148",
                    "label": "plug-in"
                }
            ],
            "schema:citation": "Linssen, Charl et al. (2018). NEST 2.16.0. Zenodo. 10.5281/zenodo.1400175",
            "schema:code": {
                "@id": "https://github.com/nest/nest-simulator"
            },
            "schema:copyrightYear": 2018,
            "schema:dateCreated": "2018-08-21",
            "schema:description": "NEST is a highly scalable simulator for networks of point or few-compartment spiking neuron models. It includes multiple synaptic plasticity models, gap junctions, and the capacity to define complex network structure.",
            "schema:device": [
                {
                    "@id": "https://www.wikidata.org/wiki/Q5082128",
                    "label": "mobile device"
                }
            ],
            "schema:documentation": {
                "@id": "http://www.nest-simulator.org/documentation/"
            },
            "schema:encodingFormat": [
                {
                    "@id": "https://www.wikidata.org/wiki/Q28865",
                    "label": "Python"
                }
            ],
            "schema:headline": "NEST is a highly scalable simulator for networks of point or few-compartment spiking neuron models. It includes multiple synaptic plasticity models, gap junctions, and the capacity to define complex network structure.",
            "schema:identifier": [
                {
                    "schema:propertyID": "doi",
                    "schema:value": "10.5281/zenodo.1400175"
                },
                {
                    "@id": "https://doi.org/10.5281/zenodo.1400175"
                }
            ],
            "schema:image": {
                "@id": "http://www.nest-simulator.org/wp-content/uploads/nest-simulated-www-320.png"
            },
            "schema:isAccessibleForFree": true,
            "schema:keywords": "simulation, NEST",
            "schema:programmingLanguage": [
                {
                    "@id": "https://www.wikidata.org/wiki/Q28865",
                    "label": "Python"
                }
            ],
            "schema:license": {
                "@id": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
                "label": "GNU General Public License 2 or later (http://www.nest-simulator.org/license/)"
            },
            "schema:name": "NEST v2.16.0",
            "schema:operatingSystem": [
                {
                    "@id": "http://dbpedia.org/resource/Linux",
                    "label": "Linux"
                }
            ],
            "schema:releaseNotes": "https://github.com/nest/nest-simulator/releases/tag/v2.16.0",
            "schema:screenshot": {
                "@id": "http://www.nest-simulator.org/wp-content/uploads/nest-simulated-www-320.png"
            },
            "schema:softwareHelp": {
                "@id": "http://www.nest-simulator.org/community/"
            },
            "schema:softwareRequirements": "libreadline, gsl, ...",
            "schema:url": {
                "@id": "http://www.nest-simulator.org/"
            },
            "schema:version": "2.16.0"
        }
        """)
        instance = MockInstance(instance_data)
        software_release = Software.from_kg_instance(instance, client=None, use_cache=False)
        assert software_release.name == instance_data["schema:name"]
        assert software_release.operating_system == OperatingSystem("Linux")
