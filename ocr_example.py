from PIL import Image
import pytesseract
import os

if __name__ == "__main__":
    sample = pytesseract.image_to_string(Image.open("./split-images/0001/Entity1.jpg"))

    sampleFile = open("0001_ocr_sample.txt", "w")

    for line in sample.split("\n"):
        if not line.strip():
            continue 
        sampleFile.write(line + "\n")

    sampleFile.close()