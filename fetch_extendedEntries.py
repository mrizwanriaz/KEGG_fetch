import requests
import time
import sys

def fetch_reaction_entries():
    print("Downloading reaction-associated data")
    # get reaction equations, RCLASS, and reaction-metabolite data
    fetch_reaction_info("reaction.txt")
    # get reaction enzymes
    fetch_reaction_enzymes()
    # get reaction orthology
    fetch_reaction_orthology()

    print("Reaction entries downloaded")

def fetch_organism_entries():
    print("Downloading EC, KO, Pathway entries for each organism")
    with open('organism.txt', 'r') as list_file:
        ids = list_file.readlines()

    # list of DB entries
    entries = ['ec', 'ko', 'pathway']

    for entry in entries:
        # create text file
        new_file = open('organism_' + entry + '.txt', 'w')

        for line in ids:
            organism_id = line.split("\t")[1].strip()

            try:
                # get page data
                response = requests.get(f'http://rest.kegg.jp/link/{entry}/{organism_id}')
                data = response.text
                # write file
                new_file.write(data)
            except requests.RequestException as e:
                print(f"Failed: http://rest.kegg.jp/link/{entry}/{organism_id}")
                print(f"Error: {e}")

        # close file
        new_file.close()

    # create organism-reaction file based on org-ko and rxn-ko mapping
    create_organism_reactions()
    print("Organism entries downloaded")

def fetch_pathway_entries():
    print("Downloading pathway entries")
    fetch_pathway_metabolite()
    fetch_pathway_enzyme()
    fetch_pathway_reactions()
    download_ref_kgml_files()
    print("Done")

def fetch_reaction_info(reactions_file):
    print("Downloading reaction equations, metabolite, and RPAIRs")
    with open(reactions_file, 'r') as list_file:
        ids = list_file.readlines()

    rxn_equation_file = open('reaction_equations.txt', 'w')
    rxn_pair_file = open('reactant_pairs.txt', 'w')
    rxn_metabolite_file = open('reaction_metabolites.txt', 'w')

    for line in ids:
        reaction_id = line.split("\t")[0].strip()

        try:
            # get page data
            response = requests.get(f'http://rest.kegg.jp/get/{reaction_id}')
            data = response.text

            for data_line in data.split("\n"):
                data_line = data_line.strip()

                # write reaction equation
                if data_line.startswith("EQUATION"):
                    equation = data_line.replace("EQUATION", "").strip()
                    rxn_equation_file.write(f"{reaction_id.replace('rn:', '')}\t{equation}\n")

                    # create reaction-metabolite table entry
                    substrates, products = [s.strip() for s in equation.split('=')]

                    for substrate in substrates.split(" + "):
                        role = "S"
                        substrate = substrate.replace("<", "").strip()
                        sub_cols = substrate.split()
                        n = "1" if len(sub_cols) == 1 else sub_cols[0]
                        rxn_metabolite_file.write(f"{reaction_id.replace('rn:', '')}\t{substrate}\t{n}\t{role}\tY\n")

                    for product in products.split(" + "):
                        role = "P"
                        product = product.replace(">", "").strip()
                        prod_cols = product.split()
                        n = "1" if len(prod_cols) == 1 else prod_cols[0]
                        rxn_metabolite_file.write(f"{reaction_id.replace('rn:', '')}\t{product}\t{n}\t{role}\tY\n")

                # write RPAIR entry
                elif data_line.startswith("RCLASS"):
                    rpair = data_line.replace("RCLASS", "").strip()
                    rxn_pair_file.write(f"{reaction_id.replace('rn:', '')}\t{rpair}\n")

        except requests.RequestException as e:
            print(f"Error occurred while downloading {reaction_id}")
            print(f"Error: {e}")

    rxn_equation_file.close()
    rxn_metabolite_file.close()
    rxn_pair_file.close()
    print("Done.")

def download_ref_kgml_files():
    print("Downloading pathway KGML files")
    with open('keggpathways.txt', 'r') as list_file:
        pathways = list_file.readlines()

    # create folder to store KGML files
    os.makedirs("KGML_files", exist_ok=True)
    
    counter = 0
    for line in pathways:
        pathway_id = line.split()[0]

        try:
            # get page data
            response = requests.get(f'http://rest.kegg.jp/get/rn{pathway_id}/kgml')
            data = response.text

            with open(f"KGML_files/{pathway_id}.kgml", "w") as new_file:
                new_file.write(data)

            counter += 1

        except requests.RequestException as e:
            print(f"Error occurred while downloading KGML file of {pathway_id}")
            print(f"Error: {e}")

    print(f"{counter} KGML files downloaded!")


def fetch_reaction_enzymes():
    response = requests.get('http://rest.kegg.jp/link/ec/rn')
    data = response.text
    # write file
    new_file = open('reaction_enzymes.txt', 'w')
    new_file.write(data)
    new_file.close()

def fetch_reaction_orthology():
    print("Fetching Reaction KO links")
    response = requests.get('http://rest.kegg.jp/link/ko/rn')
    data = response.text
    # write file
    new_file = open('keggorthology_reactions.txt', 'w')
    new_file.write(data)
    new_file.close()
    print("Done")

def fetch_pathway_metabolite():
    response = requests.get('http://rest.kegg.jp/link/cpd/pathway')
    data = response.text
    # write file
    new_file = open('pathway_metabolites.txt', 'w')
    new_file.write(data)
    new_file.close()

def fetch_pathway_enzyme():
    print("Fetching Pathways Enzymes")
    response = requests.get('http://rest.kegg.jp/link/ec/pathway')
    data = response.text
    # write file
    new_file = open('pathway_enzymes.txt', 'w')
    new_file.write(data)
    new_file.close()
    print("Done")

def fetch_pathway_reactions():
    print("Fetching reactions involved in each pathway")
    response = requests.get('http://rest.kegg.jp/link/rn/pathway')
    data = response.text
    # write file
    new_file = open('pathway_reactions.txt', 'w')
    new_file.write(data)
    new_file.close()
    print("Done")

def create_organism_reactions():
    print("Building Organism-Reaction relation table")
    ko_rxn_dict = {}

    with open("keggorthology_reactions.txt", "r") as koRxnFile:
        for line in koRxnFile:
            cols = line.split()
            ko = cols[1].replace("ko:", "").strip()
            rxn = cols[0].replace("rn:", "")
            if ko in ko_rxn_dict:
                ko_rxn_dict[ko].append(rxn)
            else:
                ko_rxn_dict[ko] = [rxn]

    new_file = open("organism_reaction.txt", "w")  # new file

    with open("organism_ko.txt", "r") as koOrgFile:
        for line in koOrgFile:
            cols = line.split()
            ko = cols[1].replace("ko:", "").strip()
            org_code = cols[0].split(":")[0]  # get org code
            if ko in ko_rxn_dict:
                rxns = ko_rxn_dict[ko]  # get rxn list
                for rxn in rxns:
                    new_file.write(f"{org_code}\t{rxn}\n")

    new_file.close()
    print("Organism reactions are written successfully")

def fetch_metabolite_formulae():
    print("Extracting metabolite formulae")
    # Create text file
    new_file = open('metabolite_formulae.txt', 'w')
    
    with open('metabolites.txt', 'r') as in_file:
        for line in in_file:
            metabolite_id = line.split("\t")[0].replace("cpd:", "")
            
            try:
                # Get page data
                response = requests.get(f'http://rest.kegg.jp/get/{metabolite_id}')
                data = response.text

                for data_line in data.split("\n"):
                    data_line = data_line.strip()

                    # Write formulae for metabolites
                    if data_line.startswith("FORMULA"):
                        formula = data_line.split()[1].strip()
                        new_file.write(f"{metabolite_id}\t{formula}\n")
                        break
            except requests.RequestException as e:
                print(f"Error occurred while fetching formula for {metabolite_id}")
                print(f"Error: {e}")

    new_file.close()
    print("Formulae fetched for metabolites.")
