from lxml import etree
import lxml.etree as ET


namespaces = {
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'dc': "http://purl.org/dc/elements/1.1/",
    'dcterms': "http://purl.org/dc/terms/",
    'edm': "http://www.europeana.eu/schemas/edm/",
    'owl': "http://www.w3.org/2002/07/owl#",
    'wgs84_pos': "http://www.w3.org/2003/01/geo/wgs84_pos#",
    'ore' : "http://www.openarchives.org/ore/terms/"
}


def Search_dublincore(tree):
    dc = {
        "Title": "",
        "Type": "",
        "Location": "",
        "Description": "",
        "Date": "",
        "Format": ""
    }
    root = tree.getroot()  
    # Cerca il tag "title" all'interno del file XML
    title = root.find(".//unittitle")
    if title is not None:
        dc["Title"] = title.text
    
    # Cerca il tag "type" all'interno del file XML
    type_tag = root.find(".//type")
    if type_tag is not None:
        dc["Type"] = type_tag.text
    
    # Cerca il tag "location" all'interno del file XML
    location = root.find(".//originalsloc")
    if location is not None:
        dc["Location"] = location.text
    
    # Cerca il tag "description" all'interno del file XML
    description = root.find(".//description") 
    if description is not None:
        dc["Description"] = description.text
    
    # Cerca il tag "date" all'interno del file XML
    date = root.find(".//date")
    if date is not None:
        dc["Date"] = date.text
    
    # Cerca il tag "format" all'interno del file XML
    Web_resource = root.find(".//dao")
    if Web_resource is not None:
        dc["Format"] = Web_resource.attrib.get("href")
    return dc


xml = etree.Element("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF", nsmap=namespaces)
# carica il file XML
tree = ET.parse("EAD.xml")
root = tree.getroot()
ProvidedCHO = root.find(".//eadid")
if ProvidedCHO is not None: 
    edm_provided_cho = ProvidedCHO.attrib.get("url")

    providedCHO = etree.Element(f"{{{namespaces['edm']}}}ProvidedCHO", attrib={"{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about": edm_provided_cho})
    aggregation = etree.Element(f"{{{namespaces['ore']}}}aggregation",attrib={"{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about": edm_provided_cho})
    xml.append(providedCHO)
    xml.append(aggregation)
    aggregationCHO = etree.SubElement(aggregation,f"{{{namespaces['edm']}}}aggregatedCHO",attrib={"{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about": edm_provided_cho})
# Crea il tag web resource
Web_resource = root.find(".//dao")
if Web_resource is not None:
    Edm_Web_resource = Web_resource.attrib.get("href")
    web_resource = etree.Element(f"{{{namespaces['edm']}}}WebResource", attrib={"{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about": Edm_Web_resource})
    xml.append(web_resource)
    edm_is_shown_by = etree.SubElement(aggregation,f"{{{namespaces['edm']}}}isShownBy", attrib={"{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about": Edm_Web_resource})
 


    # Inserisce i dublin core
    proxy = etree.Element(f"{{{namespaces['ore']}}}proxy", nsmap=namespaces)
    for dc_key, dc_value in Search_dublincore(tree).items():
        if dc_value:
            dc_element = etree.Element(f"{{{namespaces['dc']}}}{dc_key}")
            dc_element.text = dc_value
            web_resource.append(dc_element)
            providedCHO.append(dc_element)
    xml.append(proxy)
  
    
         

        

with open("EDM_out.xml", "wb") as f:
    f.write(etree.tostring(xml, pretty_print=True))

1