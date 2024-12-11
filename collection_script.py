import requests

URL = "https://nec-por.ne-compass.com/NEC.XmlDataPortal/api/c2c?networks=Maine&dataTypes=cctvSnapshotData"

def download_xml_file(url, output_file):
    try:
        response = requests.get(url)

        response.raise_for_status()

        with open(output_file, 'wb') as file:
            file.write(response.content)

        print(f'XML successfully downloaded and saved as "{output_file}".')

    except requests.exceptions.RequestException as e:
        print(f'An error ocurred while handling {output_file}: {e}')

def main():
    download_xml_file(URL, 'test.xml')

if __name__ == '__main__':
    main()
