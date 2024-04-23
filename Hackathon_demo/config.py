import lxml.etree as ET
import configparser

#ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")

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

    root[x][y].text = '8.40.9999999-SNAPSHOT'
    print(root[x][y].text)
   
    # Write changes back to the file
    tree.write(file_name, xml_declaration=True, encoding='UTF-8', standalone= False, pretty_print=True)


def update_omni_repo(omni_dependency_file, target_branch):
    config = configparser.ConfigParser()
    config.read(omni_dependency_file)

    new_baseurl = 'https://ci-artifacts05.vse.rdlabs.hpecorp.net/redfish-server-adapter/' + target_branch

    config.set('RASRepo', 'baseurl', new_baseurl)

    with open(omni_dependency_file, 'w') as configfile:
        config.write(configfile)

xml_file_paths = ['Hackathon_demo/dependencies_files/test_xml.xml', 'Hackathon_demo/dependencies_files2/test_xml2.xml']

for file in xml_file_paths:
    rename_xml_files(file)

update_omni_repo('Hackathon_demo/omni_dependency_file/dependencies.repo', 'rel/8.60/YUM/Build/0484xxx/')
