import json
import numpy as np

def convertJsonToArray(imgName):
    with open('json/' + imgName + '.json') as jsonFile:
        imageAttributes  = json.loads(jsonFile.read()) 
    return [imageAttributes["numEntity"],imageAttributes["numRelationship"],imageAttributes["numAttributes"]]


def main():
    array = []
    for i in range(1, 168):
        array.append(convertJsonToArray(str(i).zfill(4)))
    return np.array(array)

print(main())