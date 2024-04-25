import requests
import lxml.etree as ET
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import re


# Suppress insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    
from bs4 import BeautifulSoup

def get_latest_build(url):
    response = requests.get(url,verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        files = [link.get('href') for link in soup.find_all('a')]
        base_folders = [os.path.basename(os.path.normpath(path)) for path in files]
        pattern = re.compile(r'^\d+\.\d+\.\d+$')
        folders = [path for path in base_folders if pattern.match(path)]
        latest_build = max(folders)
        return latest_build
    else:
        print("Failed to fetch data from the URL.")
        return None

url = "https://ci-nexus.vse.rdlabs.hpecorp.net/nexus/content/repositories/releases/com/hp/ci/platform/lib/ris-sdk/"
print("started")
latest_version = get_latest_build(url)
print(latest_version)

def update_ras_files():
    ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")

    def rename_xml_files(file_name):
        # Parse the XML file
        tree = ET.parse(file_name)

        # Get the root element
        root = tree.getroot()
        x = 0
        y = 0


        for attributes in root:
            if 'properties' in attributes.tag:
                break
            x += 1

        for tags in root[x]:
            if 'atlasDependencyVersion' in tags.tag:
                break
            y += 1

        root[x][y].text = latest_version
        print(root[x][y].text)
   
        # Write changes back to the file
        tree.write(file_name, xml_declaration=True, encoding='UTF-8', standalone= False, pretty_print=True)

   xml_file_paths = ['Hackathon_demo/dependencies_files/test_xml.xml', 'Hackathon_demo/dependencies_files2/test_xml2.xml']

    for file in xml_file_paths:
        rename_xml_files(file)

update_ras_files()
