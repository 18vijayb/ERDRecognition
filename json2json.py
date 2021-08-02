'''
@author Mohamed Bah
@version 08/01/2021

The purpose of this code is convert the gcp generated json files into a more filtered
json file for clustering
'''

import json, os

filepath_dir = os.getcwd() + "/Images"
dest_dir = os.getcwd() + "/json"

def jsonGenerator(fileName):
    # Opening json file
    f = open(fileName)

    # Returns json object as a dictionary
    data = json.load(f)

    numEntity = 0
    numRelationship = 0
    numAttributes = 0

    # Iterates through the json list
    for i in data['displayNames']:
        if i == 'Entity':
            numEntity += 1
        elif i == 'Relationship':
            numRelationship += 1
        else:
            numAttributes += 1

    print(numEntity, numRelationship, numAttributes)

    data = {}
    data['filepath'] = filepath_dir
    data['filename'] = os.path.basename(fileName)[:-4] + "jpg"
    data['numEntity'] = numEntity
    data['numRelationship'] = numRelationship
    data['numAttributes'] = numAttributes

    outFile = dest_dir + "/" + os.path.basename(fileName)

    with open(outFile, 'w') as file:
        json.dump(data, file)

    # Closing file
    f.close()

jsonGenerator('gcpsample.json')
print()

json_dir =  os.getcwd() + "/response"
    
for fileName in os.listdir(json_dir):
    if fileName.endswith(".json"):
        jsonGenerator(json_dir + "/" + fileName)

'''
The Sample json file to be generated:

{
  "filepath": "PATH_TO_FILE",
  "filename": "0001.jpg",
  "numEntities": 5,
  "numRelationships": 4,
  "numAttributes": 2,
  "entities": [
    {
      "name": "Food Item",
      "primaryKey": "Name",
      "numEntityAttributes": 2,
      "entityAttributes": [
        "Price", 
        "Number of Calories"
      ]
    }
  ],
  "relationships": [
    "Usual Side",
    "Supervises",
    etc.
  ],
  "attributes": [
    "String 1",
    "String 2",
    etc.
  ],
}
'''