from lxml import etree
import lxml.etree as ET
import json   #FUNZIONANTE

# carica il file XML
tree = ET.parse("EAD_output_tesi3.xml")#generato da iiif_to ead
root = tree.getroot()
number = input("inserisci ")
dao_list = root.findall(".//dao[@href]")
dao_ids = [dao.attrib["href"] for dao in dao_list]

# Creazione del dizionario vuoto per memorizzare i dati
data = {
    "@id" : f"https://iiif.crystalbridges.org/{number}/manifest.json",
    "@context": f"http://iiif.io/api/presentation/{number}/context.json",
    "@type": "sc:Manifest",
    "sequences": [{
        "canvases": [
            
        ]
    }],
    "items": [],
   
    "metadata": []
}

# Loop sui tag "unittitle" e memorizzazione dei loro contenuti in un dizionario
for unittitle in root.iter('unittitle'):
    label = unittitle.attrib.get('label', '')
    content = unittitle.text.strip() if unittitle.text else ''
    data["items"].append({"label": label, "content": content})
    #data["sequences"][0]["canvases"][0]["images"][0]["on"] = f"http://localhost/~salvatore/{number}/index.json/canvas/{content}"
    data["items"].append({"id": f"http://localhost/~salvatore/{number}/index.json/canvas/{content}", "type": "Canvas"})
   
    metadata_dict = {"label": label, "value": content, "type": "simple"}
    data["metadata"].append(metadata_dict)
# Aggiungi gli elementi a `images` all'interno del dizionario `metadata`

# Loop sui dao_id e creazione degli elementi "image" per ogni dao_id
for dao_id in dao_ids:
    number = int(number) + 1
    
    filename = dao_id.split(".jp2")[0] + ".jp2"
    image = {
      
      "@id": f"https://www.e-codices.unifr.ch/metadata/iiif/{number}mgb-0382/canvas/mgb-0382_e001.json",
      "label": "Hospital. Cambridge, Addenbrookes , Cambs, UK (35kAB034)",
      "@type": "sc:Manifest",
      "width": 7235,
      "height": 4701,
      "images": [{
        
        
        "resource": {
            "@id": dao_id,
            "type": "dctypes:Image",
            "format": "image/jpeg",
            "service": {
                "@context": "http://iiif.io/api/image/2/context.json",
                "@id": filename,#cosi facendo funziona solo per jp2 per tif no
                "profile": "http://iiif.io/api/image/2/level1.json"
            }
        },
        "on": "",
        "motivation": "sc:painting"
      }]
    }
    data["sequences"][0]["canvases"].append(image)
    

# Stampa il dizionario `data`
print(data)

# Salva il dizionario `data` in un file JSON
with open("dato_nuovo45.json", "w") as outfile:
    json.dump(data, outfile)
