import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        filename="gs://cloud-ai-platform-a6082487-cf12-4655-936f-3145ead10e44/"+root.find('filename').text
        for member in root.findall('object'):
            value = (filename,
                     member[0].text,
                     int(member[4][0].text)/int(root.find("size")[0].text),
                     int(member[4][1].text)/int(root.find("size")[1].text),
                     "",
                     "",
                     int(member[4][2].text)/int(root.find("size")[0].text),
                     int(member[4][3].text)/int(root.find("size")[1].text),
                     "",
                     "",
                     )
            xml_list.append(value)
    column_name = ['GCS_FILE_PATH', 'LABEL', 'X_MIN', 'Y_MIN', "BLANK", "BLANK2", 'X_MAX', 'Y_MAX',"BLANK3", "BLANK4"]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    image_path = os.path.join(os.getcwd(), 'images')
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv(('images/image_labels.csv'), index=None)
    print('Successfully converted xml to csv.')


main()
