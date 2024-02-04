import requests
import json

def fetch_kegg_info():
    # Fetch KEGG database information
    print("Getting KEGG database info...")
    response = requests.get("http://rest.kegg.jp/info/kegg")
    data = response.text.splitlines()[1]
    release_info = data.replace("kegg", "").strip()
    print('Kegg Info: '+ release_info)
   

# Get organisms
def fetch_all_organisms():
    # Fetch all organisms from KEGG
    print("Fetching all organism from KEGG...")
    response = requests.get("http://rest.kegg.jp/list/organism")
    data = response.text

    with open("organism.txt", "w") as org_file:
        org_file.write(data)

    print("Done.")

# Get metabolites
def fetch_all_metabolites():
    # Fetch all metabolites from KEGG
    print("Fetching metabolites from KEGG...")
    response = requests.get("http://rest.kegg.jp/list/cpd")
    data = response.text

    with open("metabolites.txt", "w") as cpd_file:
        cpd_file.write(data)

    print("Done.")

# Get pathways
def fetch_all_pathways():
    # Fetch all pathways from KEGG
    print("Fetching pathways from KEGG...")
    response = requests.get("http://rest.kegg.jp/get/br:br08901/json")
    data = response.json()

    with open("keggpathways.txt", "w") as pw_file:
        metabolism = data['children'][0]['children']
        for pset in metabolism[1:]:
            set_name = pset['name']
            if "Chemical structure transformation maps" not in set_name:
                for pathway in pset['children']:
                    pw_file.write(pathway['name'] + "\t" + set_name + "\n")

    print("Done.")

# Get reactions
def fetch_all_reactions():
    # Fetch all reactions from KEGG
    print("Fetching reactions from KEGG...")
    response = requests.get("http://rest.kegg.jp/list/rn")
    data = response.text

    with open("reaction.txt", "w") as rn_file:
        rn_file.write(data)

    print("Done.")

# Get enzymes
def fetch_all_enzymes():
    # Fetch all enzymes from KEGG
    print("Fetching enzymes from KEGG...")
    response = requests.get("http://rest.kegg.jp/list/enzyme")
    data = response.text

    with open("enzyme.txt", "w") as rn_file:
        rn_file.write(data)

    print("Done.")
