import argparse
import os 
import json
from PIL import Image


def splitImage(imgName):
    with open('response/' + imgName + '.json') as jsonFile:
        data = jsonFile.read() 
        data = data.replace("\'", "\"")
        data = json.loads(data) 
    with open('response/' + imgName + '.json', 'w') as jsonFile:
        json.dump(data, jsonFile)

#    jsonFile = open('response/' + imgName + '.json').read()
    

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

if __name__ == "__main__":

    # TODO: Arg parsing
    '''
    parser = argparse.ArgumentParser(prog='imgsplit',
                                     usage='%(prog)s <file-path>',
                                     description='Process a JSON file generated from model')

    parser.add_argument('-f', metavar='<file-path>', type=str, nargs='+',
                        help='path to image recognition json file')

    if args.
    print(args.accumulate(args.integers))
    ''' 
    for i in range(1, 168):
        splitImage(str(i).zfill(4))
    
