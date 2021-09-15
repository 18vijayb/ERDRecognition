'''
# @author Bradley Bottomlee, Vijay Bharadwaj, Mohamed Bah 
#
# This file runs the py tesseract OCR library on every object in the dataset and writes the results to their respective files
# TODO: Make this code apart of the main pipeline 
#
'''

from PIL import Image
import pytesseract
import os

if __name__ == "__main__":

    rootDir = "./split-images/"
    outputDir = "./text/"
    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            filePath = os.path.join(subdir, file)
            filePathSplit = filePath.split('/')

            if len(filePathSplit) < 3:
                continue 

            imgName = filePathSplit[2]
            outputPath = filePath[len(rootDir):len(filePath) - 4] + '.txt'

            try:
                ocrText = pytesseract.image_to_string(Image.open(filePath))
            except:
                continue
            
            try:
                os.mkdir(outputDir + imgName)
            except FileExistsError:
                continue
             
            with open(outputDir + outputPath, 'w') as ocrTextOutputFile:            
                for line in ocrText.split("\n"):
                    if not line.strip():
                        continue 
                    ocrTextOutputFile.write(line + "\n")
