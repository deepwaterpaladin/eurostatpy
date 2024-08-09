import xml.etree.ElementTree as ET

def parse_xml_to_dict(element, namespaces, language:str=None):
    result = {}
    if element.tag == f"{{{namespaces['nt']}}}leaf" and (element.attrib.get('type') == 'table' or element.attrib.get('type') == 'dataset'):
        titles = element.findall(f".//nt:title", namespaces)
        code = element.find("nt:code", namespaces).text

        for title in titles:
            if language is not None:
                if title.attrib.get("language") == language:
                    name = title.text
                    result[name] = code
            else:
                name = title.text
                result[name] = code

    for child in element:
        result.update(parse_xml_to_dict(child, namespaces, language))

    return result

def read_xml_to_dict(file_path:str, language:str=None):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'nt': 'urn:eu.europa.ec.eurostat.navtree'}

    return parse_xml_to_dict(root, namespaces, language)
