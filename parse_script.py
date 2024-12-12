import xml.etree.ElementTree as ET
import base64
import re
from PIL import Image, ImageFile, ExifTags
from io import BytesIO

OUTPUT = './testimages/'

def basicParse(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    namespace = {'ns': 'http://its.gov/c2c_icd'}
    
    return(root, namespace)

def parseImgXML(xml, locations):
    root, namespace = basicParse(xml)
    for sub in root.findall('./ns:cctvSnapshotData/ns:net/ns:cctvSnapshot', namespace):
        if '295' in sub.attrib['id']:
            #print(sub.attrib['id'])
            name = sub.find('./ns:name', namespace).text
            timestamp = sub.find('./ns:timestamp', namespace).text
            snippet = sub.find('./ns:snippet', namespace).text
            
            new_name = name.replace("I-295 ", "")
            new_name = new_name = re.sub(r"\(([^)]+)\)", lambda m: f"({m.group(1).replace(' ', '')})", new_name)
            new_name = new_name.replace("(", "").replace(")", "").replace(" ", "_").replace("Mile_", "M")

            new_name += "_"+ timestamp[:-2].replace(":", "")

            if snippet: #check if image data exists
                image_data = base64.b64decode(snippet)
                with BytesIO(image_data) as image_file:
                    with Image.open(image_file) as img:
                        img.save(OUTPUT+new_name+'.jpg', "JPEG")

def parseStatusXML(xmlfile):
    locations = []
    root, namespace = basicParse(xmlfile)
    for sub in root.findall('./ns:cctvStatusData/ns:net/ns:cctvStatus', namespace):
        if '295' in sub.attrib['id']:
            #print(sub.attrib['id'])
            locations.append(sub.attrib['id'])
    
    return locations 

def main():
    locations = parseStatusXML('cam_status_20241212.xml')
    parseImgXML('test.xml', locations)

if __name__ == '__main__':
    main()