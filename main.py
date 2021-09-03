'''
# @author Bradley Bottomlee, Vijay Bharadwaj, Mohamed Bah 
#
# This file runs the entire ERD recognition pipeline (i.e., request to model endpoint, response processing, and clustering)
#
#
'''

import base64, argparse, json, os
import numpy as np

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from PIL import Image

_endpoint_id = ""
_location = ""
_project = ""
_source_dir = ""
_dest_dir = ""

def predict_image_object_detection_sample(
    project: str,
    endpoint_id: str,
    filename: str,
    dest: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageObjectDetectionPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_object_detection_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageObjectDetectionPredictionParams(
        confidence_threshold=0.9, max_predictions=100,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    #print("response")
    #print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_object_detection.yaml for the format of the predictions.
    predictions = response.predictions
    with open(dest, 'w') as f:
        for prediction in predictions:
            f.write(str(dict(prediction)))  

def splitImage(imgName):
    with open(_dest_dir + imgName + '.json') as jsonFile:
        data = jsonFile.read() 
        data = data.replace("\'", "\"")
        data = json.loads(data) 
    with open(_dest_dir + imgName + '.json', 'w') as jsonFile:
        json.dump(data, jsonFile)    

    boxes = data['bboxes']
    objects = data['displayNames']
    if not os.path.exists('split-images/'):
        os.mkdir('split-images')
    if not os.path.exists('split-images/' + imgName):
        os.mkdir('split-images/' + imgName)

    # Opens an image 
    im = Image.open('images/' + imgName + '.jpg')
    width, height = im.size

    counter = 0
    for box, displayName in zip(boxes, objects):
        counter += 1
        yCoordinates = [box[2], box[3]]
        xCoordinates = [box[0], box[1]]

        left = min(xCoordinates) * width
        top = min(yCoordinates) * height
        right = max(xCoordinates) * width 
        bottom = max(yCoordinates) * height
        im1 = im.crop((left, top, right, bottom))
        im1.save('split-images/' + imgName + '/' + displayName + str(counter) + '.jpg')

def jsonGenerator(fileName, filePathDir, destDir):
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

    #print(numEntity, numRelationship, numAttributes)

    data = {}
    data['filepath'] = filePathDir
    data['filename'] = os.path.basename(fileName)[:-4] + "jpg"
    data['numEntity'] = numEntity
    data['numRelationship'] = numRelationship
    data['numAttributes'] = numAttributes

    outFile = destDir + "/" + os.path.basename(fileName)

    with open(outFile, 'w') as file:
        json.dump(data, file)

    # Closing file
    f.close()

def convertJsonToArray(imgName):
    with open('json/' + imgName + '.json') as jsonFile:
        imageAttributes  = json.loads(jsonFile.read()) 
    return [imageAttributes["numEntity"],imageAttributes["numRelationship"],imageAttributes["numAttributes"]]

def main():
    # iterate through each image and query the model endpoint
    for file in os.listdir(_source_dir):
        if file.endswith(".jpg"):
                predict_image_object_detection_sample(
                    project= _project,
                    endpoint_id= _endpoint_id,
                    location= location,
                    filename= __source_dir + "/" + file,
                    dest = _dest_dir + "/" + file[:file.index(".jpg")] + ".json"
                )
    
    # split individual objects in each respective image 
    for i in range(1, 168):
        splitImage(str(i).zfill(4))

    # json -> json -> array
    json_dir =  os.getcwd() + "/response"
    
    for fileName in os.listdir(json_dir):
        if fileName.endswith(".json"):
            jsonGenerator(json_dir + "/" + fileName, os.getcwd() + "/images", os.getcwd() + "/json")
    
    array = []
    for i in range(1, 168):
        array.append(convertJsonToArray(str(i).zfill(4)))

    jsonArray = np.array(array)
    print(jsonArray)

if __name__ == "__main__":
    # TODO: Implement config handling (i.e., read from a file certain values such as model endpoint)
    _source_dir = os.getcwd() + "/Dataset_Spring2021_HW4_Q1"
    _dest_dir = os.getcwd() + "/response/"
    _endpoint_id = "3953439193203474432"
    _location = "us-central1"
    _project = "844474434394"

    main() 