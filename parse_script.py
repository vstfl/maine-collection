import xml.etree.ElementTree as ET
import base64
from PIL import Image, ImageFile, ExifTags
from io import BytesIO

OUTPUT = './testimages/'

def parseXML(xmlfile):

    tree = ET.parse(xmlfile)
    root = tree.getroot()
    namespace = {'ns': 'http://its.gov/c2c_icd'}
    
    for sub in root.findall('./ns:cctvSnapshotData/ns:net/ns:cctvSnapshot', namespace):
        if '295' in sub.attrib['id']:
            #print(sub.attrib['id'])
            name = sub.find('./ns:name', namespace).text
            timestamp = sub.find('./ns:timestamp', namespace).text
            snippet = sub.find('./ns:snippet', namespace).text

            if snippet:
                image_data = base64.b64decode(snippet)
                with BytesIO(image_data) as image_file:
                    with Image.open(image_file) as img:

                        #exif_data = ExifTags.TAGS.get(36867, 'DateTimeOriginal')

                        img.save(OUTPUT+name+'.jpg', "JPEG")

def main():
    parseXML('test.xml')

if __name__ == '__main__':
    main()