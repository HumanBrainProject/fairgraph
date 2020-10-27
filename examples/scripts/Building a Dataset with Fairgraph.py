#!/usr/bin/env python
# coding: utf-8

# # Caveats
# > Checks for instance existence using 'name' field
# 
# >All empty fields replaced with None value

# # Install Fairgraph and Dependencies

# In[1]:


get_ipython().run_cell_magic('capture', '', '!rm -rf fairgraph\n!git clone -b master https://github.com/GMattheisen/fairgraph.git\n!pip install -r ./fairgraph/requirements.txt\n!pip install -U ./fairgraph')


# In[2]:


get_ipython().run_cell_magic('capture', '', '!rm -rf pyxus\n!git clone -b master https://github.com/GMattheisen/pyxus.git\n!pip install -U ./pyxus')


# # Imports + Logging
# > Import the necessary Python libraries and initiate logging module to help resolve errors

# In[50]:


"""
###############################################
### Building a dataset object with fairgraph ###
###############################################
"""
import os, time
from datetime import datetime
import csv
import logging
import pandas as pd
from fairgraph import uniminds, KGClient, minds

logging.basicConfig(filename="to_knowledge_graph.log",
                    filemode='a',
                    level=logging.DEBUG)

logger = logging.getLogger("nar")

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJicC1vaWRjIn0.eyJleHAiOjE1ODQwMzEwMTgsInN1YiI6IjMwODEwNSIsImF1ZCI6WyIzMjMxNDU3My1hMjQ1LTRiNWEtYjM3MS0yZjE1YWNjNzkxYmEiXSwiaXNzIjoiaHR0cHM6XC9cL3NlcnZpY2VzLmh1bWFuYnJhaW5wcm9qZWN0LmV1XC9vaWRjXC8iLCJqdGkiOiI2N2Y2OTMwNy1lNzc5LTQzMTItOWMyYS1hNTM2M2E2ODgyNTYiLCJpYXQiOjE1ODQwMTY2MTgsImhicF9rZXkiOiJhN2QwNmFlZTMyOGI3YjkzNTc3OTUxNzU2Mjk2ODc3YjE4YzRmYTFjIn0.A04N8tLAr-UW6R7W3b-yzuNrW7DI4vsDULH0SJNr7cTvrvMTtkfoQkvWM-JFz3BvegXjXAxzs4lF5wMQhqSWtCShkpwnNsqa9elr2b-xfGVoYluAaQc2TU2ubNbI0VD72kZ5ircliV00L60dXyYuLGdNUz5reM9f0QS4Sw0hiDA"
client = KGClient(token, nexus_endpoint='https://nexus-int.humanbrainproject.org/v0')


# # Load the Metadata Form
# > Metadata is loaded from a CSV file and saved as key: value entries in a dictionary

# In[26]:


reader = csv.reader(open('test_dataset.csv', 'r'))
data = {}
for row in reader:
   k, v = row
   data[k.lower().strip().replace(" ","_")] = v
    
data = {k: None if not v else v for k, v in data.items() } # replace empty values with None


# In[27]:


data


# # Build instances from Metadata Form
# > The data dictionary is used to populate different fields for the dataset instance

# ### Contributors

# In[28]:


if data['number_of_contributors'] != 0:
    contributors = [] # create a list of all contributors in the data dictionary
    for i in range(int(data['number_of_contributors'])):
        if minds.Person.by_name(data[f"contributor{i+1}_name"], client) is None: # if Person not already an instance
            contributor = minds.Person(identifier=data[f"contributor{i+1}_identifier"],
                                  name = data[f"contributor{i+1}_name"],
                                   shortname = data[f"contributor{i+1}_shortname"])
            contributor.save(client) # create Person instance
        else:
            contributor = minds.Person.by_name(data[f"contributor{i+1}_name"], client) # locate Person instance
    contributors.append(contributor) # add all to contributors list
else:
    contributors = None
print(contributors) 


# ### Owners

# In[29]:


if data['number_of_owners'] != 0:
    owners = [] # create a list of all owners in the data dictionary
    for i in range(int(data['number_of_owners'])):
        if minds.Person.by_name(data[f"owner{i+1}_name"], client) is None: # if Person not already an instance
            owner = minds.Person(identifier=data[f"owner{i+1}_identifier"],
                                  name = data[f"owner{i+1}_name"],
                                   shortname = data[f"owner{i+1}_shortname"])
            owner.save(client) # create Person instance
        else:
            owner = minds.Person.by_name(data[f"owner{i+1}_name"], client) # locate Person instance
        owners.append(owner) # add all to owners list
else:
    owners = None
print(owners)


# ### Parcellation Atlases

# In[30]:


if data['number_of_parcellation_atlases'] != 0:
    parcellation_atlases = [] # create a list of all parcellation atlases in the data dictionary
    for i in range(int(data['number_of_parcellation_atlases'])):
        if minds.ParcellationAtlas.by_name(data[f"parcellation_atlas{i+1}_name"], client) is None: # if Person not already an instance
            parcellation_atlas = minds.ParcellationAtlas(identifier = data[f'parcellation_atlas{i+1}_identifier'], 
                                                         name = data[f'parcellation_atlas{i+1}_name'])
            parcellation_atlas.save(client) # create Person instance
        else:
            parcellation_atlas = minds.ParcellationAtlas.by_name(data[f'parcellation_atlas{i+1}_name'], client)
        parcellation_atlases.append(parcellation_atlas)
else:
    parcellation_atlases = None
print(parcellation_atlases)


# ### Parcellation Regions

# In[31]:


if data['number_of_parcellation_regions'] != 0:
    parcellation_regions = [] # create a list of all parcellation atlases in the data dictionary
    for i in range(int(data['number_of_parcellation_regions'])):
        if minds.ParcellationRegion.by_name(data[f"parcellation_region{i+1}_name"], client) is None: # if Person not already an instance
            if data[f'parcellation_region{i+1}_species'] != None:
                species = Species(data[f'parcellation_region{i+1}_species'])
            else:
                species = None
            parcellation_region = minds.ParcellationRegion(identifier = data[f'parcellation_region{i+1}_identifier'], 
                                                          name = data[f'parcellation_region{i+1}_name'],
                                                          url=data[f'parcellation_region{i+1}_url'],
                                                          species=species,
                                                          alias=data[f'parcellation_region{i+1}_alias'])
            parcellation_region.save(client) # create Person instance
        else:
            parcellation_region = minds.ParcellationRegion.by_name(data[f'parcellation_region{i+1}_name'], client)
        parcellation_regions.append(parcellation_region)
else:
    parcellation_regions = None
print(parcellation_regions)


# ### Modalities

# In[32]:


if data['number_of_modalities'] != 0:
    modalities = [] # create a list of all modalities in the data dictionary
    for i in range(int(data['number_of_modalities'])):
        if minds.Modality.by_name(data[f"modality{i+1}_name"], client) is None: # if Modality not already an instance
            modality = minds.Modality(identifier = data[f'modality{i+1}_identifier'], 
                                                         name = data[f'modality{i+1}_name'])
            modality.save(client) # create Modality instance
        else:
            modality = minds.Modality.by_name(data[f'modality{i+1}_name'], client)
        modalities.append(modality)
else:
    modalities = None
print(modalities)


# ### Components

# In[33]:


if data['number_of_components'] != 0:
    components = [] # create a list of all components in the data dictionary
    for i in range(int(data['number_of_components'])):
        if minds.PLAComponent.by_name(data[f"component{i+1}_name"], client) is None: # if Component not already an instance
            component = minds.PLAComponent(identifier = data[f'component{i+1}_identifier'], 
                                            name = data[f'component{i+1}_name'],
                                            component=data[f'component{i+1}_component'],
                                            description=data[f'component{i+1}_description'])
            component.save(client) # create Component instance
        else:
            component = minds.PLAComponent.by_name(data[f'component{i+1}_name'], client)
        components.append(component)
else:
    components = None
print(components)


# ### Formats

# In[34]:


if data['number_of_formats'] != 0:
    formats = [] # create a list of all formats in the data dictionary
    for i in range(int(data['number_of_formats'])):
        if minds.Format.by_name(data[f"format{i+1}_name"], client) is None: # if format not already an instance
            format = minds.Format(identifier = data[f'format{i+1}_identifier'], 
                                                         name = data[f'format{i+1}_name'])
            format.save(client) # create Modality instance
        else:
            format = minds.Format.by_name(data[f'format{i+1}_name'], client)
        formats.append(format)
else:
    formats =None   
print(formats)


# ### Licenses

# In[35]:


if data['license_name'] != None:
    # only one License allowed
    if minds.License.by_name(data["license_name"], client) is None: # if License not already an instance
        license = minds.License(identifier = data['license_identifier'], 
                                                     name = data['license_name'])
        license.save(client) # create License instance
    else:
        license = minds.License.by_name(data[f'license_name'], client)
else:
    license = None
print(license)


# ### Publications

# In[36]:


if data['number_of_publications'] != 0:
    publications = [] # create a list of all publications in the data dictionary
    for i in range(int(data['number_of_publications'])):
        if minds.Publication.by_name(data[f"publication{i+1}_name"], client) is None: # if Publication not already an instance
            authors = []
            for b in range(int(data[f'number_of_publication{i+1}_authors'])):
                if minds.Person.by_name(data[f"publication{i+1}_author{b+1}_name"], client) is None:
                    author = minds.Person(identifier=data[f"publication{i+1}_author{b+1}_identifier"],
                                                  name = data[f"publication{i+1}_author{b+1}_name"],
                                                   shortname = data[f"publication{i+1}_author{b+1}_name"])
                    author.save(client) # create Person instance
                else:
                    author = minds.Person.by_name(data[f"publication{i+1}_author{b+1}_name"], client) # locate Person instance
                authors.append(author)

            publication = minds.Publication(identifier = data[f"publication{i+1}_identifier"], 
                                                          name = data[f"publication{i+1}_name"],
                                                          cite=data[f"publication{i+1}_cite"],
                                                          doi=data[f"publication{i+1}_doi"],
                                                          authors=authors)
            publication.save(client) # create Publication instance
        else:
            publication = minds.Publication.by_name(data[f'publication{i+1}_name'], client)
        publications.append(publication)
else:
    publications = None
    
print(publications)


# ### References Spaces

# In[37]:


if data['number_of_reference_spaces'] != 0:
    reference_spaces = [] # create a list of all ReferenceSpaces in the data dictionary
    for i in range(int(data['number_of_reference_spaces'])):
        if minds.ReferenceSpace.by_name(data[f"reference_space{i+1}_name"], client) is None: # if ReferenceSpace not already an instance
            reference_space = minds.ReferenceSpace(identifier = data[f'reference_space{i+1}_identifier'], 
                                                         name = data[f'reference_space{i+1}_name'])
            reference_space.save(client) # create ReferenceSpace instance
        else:
            reference_space = minds.ReferenceSpace.by_name(data[f'reference_space{i+1}_name'], client)
        reference_spaces.append(reference_space)
else:
    reference_spaces = None
    
print(reference_spaces)


# ### Release date

# In[38]:


if data['release_date'] != None:
    release_date = datetime.strptime(data['release_date'], '%d/%m/%y')
else:
    release_date = None


# ### Embargo status

# In[39]:


if data['embargo_status_name'] != None:
    if minds.EmbargoStatus.by_name(data['embargo_status_name'], client) is None: # if ReferenceSpace not already an instance
        embargo_status = minds.EmbargoStatus(identifier = data['embargo_status_name'], 
                                                     name = data['embargo_status_identifier'])
        embargo_status.save(client) # create ReferenceSpace instance
    else:
        embargo_status = minds.EmbargoStatus.by_name(data['embargo_status_name'], client)    
else:
    embargo_status = None

print(embargo_status)


# ### Dataset DOI

# In[40]:


if data['number_of_dataset_dois'] != 0:
    dataset_dois = []
    for i in range(int(data['number_of_dataset_dois'])):
        dataset_dois.append(data[f'dataset_doi{i+1}'])
else:
    dataset_dois = None
print(dataset_dois)


# ### Dataset Identifiers

# In[41]:


if data['number_of_dataset_identifiers'] != 0:
    dataset_identifiers = []
    for i in range(int(data['number_of_dataset_identifiers'])):
        dataset_identifier = data[f'dataset_identifier{i+1}']
    dataset_identifiers.append(dataset_identifier)
else:
    dataset_identifiers = None

print(dataset_identifiers)


# ### Specimen Group

# In[43]:


if data['number_of_specimen_groups'] != 0:
    specimen_groups = [] # create a list of all publications in the data dictionary
    for i in range(int(data['number_of_specimen_groups'])):
        if minds.SpecimenGroup.by_name(data[f'specimen_group{i+1}_name'], client) is None: # if Publication not already an instance
            subjects=[]
            for b in range(int(data[f'specimen_group{i+1}_number_of_subjects'])):                    
                if minds.Subject.by_name(data[f'specimen_group{i+1}_subject{b+1}_name'], client) is None: # if Publication not already an instance

                    """sex"""
                    if data[f'specimen_group{i+1}_subject{b+1}_sex'] != None:
                        sex=minds.Sex(data[f'specimen_group{i+1}_subject{b+1}_sex'])
                    else:
                        sex = None
                        
                    """species"""
                    if data[f'specimen_group{i+1}_subject{b+1}_species_name'] != None:
                        if minds.Species.by_name(data[f'specimen_group{i+1}_subject{b+1}_species_name'], client) is None: # if Publication not already an instance
                                species = minds.Species(name=data[f'specimen_group{i+1}_subject{b+1}_species_name'],
                                                       indentifier=data[f'specimen_group{i+1}_subject{b+1}_species_identifier'])
                                species.save(client)
                        else:
                            species = minds.Species.by_name(data[f'specimen_group{i+1}_subject{b+1}_species_name'], client)
                    else:
                        species = None
                        
                    """strains"""
                    strains = []
                    for c in range(int(data[f'specimen_group{i+1}_subject{b+1}_number_of_strains'])):
                        strains.append(data[f'specimen_group{i+1}_subject{b+1}_strains{c+1}'])

                    """age category"""
                    if data[f'specimen_group{i+1}_subject{b+1}_age_category_name'] != None:
                        if minds.AgeCategory.by_name(data[f'specimen_group{i+1}_subject{b+1}_age_category_name'], client) is None: # if Publication not already an instance
                            age_category=AgeCategory(name=data[f'specimen_group{i+1}_subject{b+1}_age_category_name'],
                                                    identifier=data[f'specimen_group{i+1}_subject{b+1}_age_category_identifier'])
                            age_category.save(client)
                        else:
                            age_category = minds.AgeCategory.by_name(data[f'specimen_group{i+1}_subject{b+1}_age_category_name'], client)
                    else:
                        age_category = None
                            
                    """identifiers"""
                    identifiers = []
                    for c in range(int(data[f'specimen_group{i+1}_subject{b+1}_number_of_identifiers'])):
                        identifiers.append(data[f'specimen_group{i+1}_subject{b+1}_identifier{c+1}'])

                    """samples"""
                    samples = []
                    for c in range(int(data[f'specimen_group{i+1}_subject{b+1}_number_of_samples'])):
                        if data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_name'] != None:
                            if minds.Sample.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_name'], client) is None: # if Publication not already an instance

                                """sample identifier"""
                                identifiers = []
                                for d in range(int(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_number_of_identifiers'])):
                                    identifier = data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_identifier{d+1}']
                                    identifiers.append(identifier)

                                """parcellation atlas"""
                                if data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_atlas_name'] != None:
                                    if minds.ParcellationAtlas.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_atlas_name']) is None:
                                        parcellation_atlas = minds.ParcellationAtlas(identifier = data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_atlas_identifier'], 
                                                     name = data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_atlas_name'])
                                        parcellation_atlas.save(client) # create Person instance
                                    else:
                                        parcellation_atlas = minds.ParcellationAtlas.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_atlas_name'])
                                else:
                                    parcellation_atlas = None
                                        
                                """methods"""
                                methods = []
                                for d in range(int(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_number_of_methods'])):
                                    if minds.Method.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_method{d+1}_name'], client) is None:
                                        method = minds.Method(name=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_method{d+1}_name'],
                                                             identifier=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_method{d+1}_identifier'])
                                        method.save(client)
                                    else:
                                        method = minds.Method.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_method{d+1}_name'], client)
                                    methods.append(method)
                                    
                                """parcellation_region"""
                                if range(int(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_number_of_parcellation_regions'])) != None:
                                    parcellation_regions = []
                                    for d in range(int(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_number_of_parcellation_regions'])):
                                        if minds.ParcellationRegion.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_name'], client) is None:
                                            if data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_species'] != None:
                                                species = Species(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_species'])
                                            else:
                                                species = None
                                            parcellation_region = minds.ParcellationRegion(identifier = data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_identifier'], 
                                                                  name = data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_name'],
                                                                  url=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_url'],
                                                                  species=species,
                                                                  alias=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_alias'])
                                            parcellation_region.save(client)
                                        else:
                                            parcellation_region = minds.ParcellationRegion.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_parcellation_region{d+1}_name'], client)
                                        parcellation_regions.append(parcellation_region)     
                                else:
                                    parcellation_regions = None
                                                                                       
                                """build sample"""
                                sample=minds.Sample(name=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_name'],
                                                    identifier=identifiers,
                                                    container_url=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_container_url'],
                                                    weight_post_fixation=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_weight_post_fixation'],
                                                    weight_pre_fixation=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_weight_pre_fixation'],
                                                    methods=methods,
                                                    parcellation_atlas=parcellation_atlas,
                                                    parcellation_region=parcellation_regions,
                                                    reference=data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_reference']
                                                   )
                                sample.save(client)
                            else:
                                sample = minds.Sample.by_name(data[f'specimen_group{i+1}_subject{b+1}_sample{c+1}_name'], client)
                            samples.append(sample)
                        else:
                            sample = None                            
                        
                    subject = minds.Subject(name=data[f'specimen_group{i+1}_subject{b+1}_name'],
                                            identifier=identifiers,
                                            strain=data[f'specimen_group{i+1}_subject{b+1}_strain'],
                                            strains=strains,
                                            cause_of_death=data[f'specimen_group{i+1}_subject{b+1}_cause_of_death'],
                                            weight=data[f'specimen_group{i+1}_subject{b+1}_weight'],
                                            age=data[f'specimen_group{i+1}_subject{b+1}_age'],
                                            age_category=age_category,
                                            samples=samples,
                                            sex=sex,
                                            species=species
                                            )
                    subject.save(client)
                    print(subject)
                else:
                    subject = minds.Subject.by_name(data[f'specimen_group{i+1}_subject{b+1}_name'], client)
            subjects.append(subject)
        
            specimen_group = minds.SpecimenGroup(identifier = data[f"specimen_group{i+1}_identifier"], 
                                                name = data[f"specimen_group{i+1}_name"],
                                                subjects=subjects)
            specimen_group.save(client) 
            
        else:
            specimen_group = minds.SpecimenGroup.by_name(data[f'specimen_group{i+1}_name'], client)
        specimen_groups.append(specimen_group)
else:
    specimen_groups = None
    
print(specimen_groups)


# ### Activity

# In[44]:


if data['number_of_activities'] != 0:
    activities = [] # create a list of all publications in the data dictionary
    for i in range(int(data['number_of_activities'])):
        if minds.Activity.by_name(data[f'activity{i+1}_name'], client) is None: 
            
            """identifier"""
            identifiers = []
            for b in range(int(data[f'activity{i+1}_number_of_identifiers'])):
                identifier = data[f'activity{i+1}_identifier{b+1}']
                identifiers.append(identifier)
                
            """ethics approval"""
            if minds.EthicsApproval.by_name(data[f'activity{i+1}_ethics_approval_name'], client) is None:
                ethics_approval = minds.EthicsApproval(name=f'activity{i+1}_ethics_approval_name',
                                                      identifier=f'activity{i+1}_ethics_approval_identifier')
                ethics_approval.save(client)
            else:
                ethics_approval= minds.EthicsApproval.by_name(data[f'activity{i+1}_ethics_approval_name'], client)
            
            """ethics authority"""
            ethics_authorities=[]
            for b in range(int(data[f'activity{i+1}_number_of_ethics_authorities'])):
                if minds.EthicsAuthority.by_name(data[f'activity{i+1}_ethics_authority{b+1}_name'], client) is None:
                    ethics_authority = minds.EthicsAuthority(name=data[f'activity{i+1}_ethics_authority{b+1}_name'],
                                                          identifier=data[f'activity{i+1}_ethics_authority{b+1}_identifier'])
                    ethics_authority.save(client)
                else:
                    ethics_authority= minds.EthicsAuthority.by_name(data[f'activity{i+1}_ethics_authority{b+1}_name'], client)
                ethics_authorities.append(ethics_authority)
            
            """preparation"""
            if minds.Preparation.by_name(data[f'activity{i+1}_preparation_name'], client) is None:
                preparation = minds.Preparation(name=f'activity{i+1}_preparation_name',
                                                      identifier=f'activity{i+1}_preparation_identifier')
                preparation.save(client)
            else:
                preparation= minds.Preparation.by_name(data[f'activity{i+1}_preparation_name'], client)
            
            """protocols"""
            protocols=[]
            for b in range(int(data[f'activity{i+1}_number_of_protocols'])):
                if minds.Protocol.by_name(data[f'activity{i+1}_protocol{b+1}_name'], client) is None:
                    protocol = minds.Protocol(name=data[f'activity{i+1}_protocol{b+1}_name'],
                                                          identifier=data[f'activity{i+1}_protocol{b+1}_identifier'])
                    protocol.save(client)
                else:
                    protocol= minds.Protocol.by_name(data[f'activity{i+1}_protocol{b+1}_name'], client)
                protocols.append(protocol)
            
            """methods"""
            methods=[]
            for b in range(int(data[f'activity{i+1}_number_of_methods'])):
                if minds.Method.by_name(data[f'activity{i+1}_method{b+1}_name'], client) is None:
                    method = minds.Method(name=data[f'activity{i+1}_method{b+1}_name'],
                                                          identifier=data[f'activity{i+1}_method{b+1}_identifier'])
                    method.save(client)
                else:
                    method= minds.Method.by_name(data[f'activity{i+1}_method{b+1}_name'], client)
                methods.append(method)
            
            
            activity = minds.Activity(name = data[f'activity{i+1}_name'],
                                     identifier=identifiers,
                                     ethics_approval= ethics_approval,
                                     ethics_authority=ethics_authorities, 
                                     methods=methods,
                                     preparation=preparation,
                                     protocols=protocols)
            activity.save(client)
        else:
            activity = minds.Activity.by_name(data[f'activity{i+1}_name'], client)
        activities.append(activity)
print(activities)


# # Create Dataset

# In[45]:


## CREATING THE DATASET
dataset = minds.Dataset(
    name=data['dataset_name'],
    description=data['dataset_description'],
    identifier=dataset_identifiers,
    container_url=data['container_url'],
    owners = owners,
    formats=formats,
    parcellation_atlas=parcellation_atlases,
    parcellation_region=parcellation_regions,
    component=components,
    license = license,
    contributors = contributors,
    modality=modalities,
    publications= publications,
    reference_space=reference_spaces,
    release_date = release_date,
    activity= activities,
    container_URL_as_ZIP= bool(data['container_url_as_zip']),
    datalink = data['datalink'],
    dataset_doi = dataset_dois,
    external_datalink=data['external_datalink'],
    doireference=data['doireference'],
    embargo_status = embargo_status,
    part_of= data['part_of'],
    specimen_group=specimen_groups
)
print(dataset)


# In[46]:


dataset.save(client) 

