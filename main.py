#main controller

import os
import fetch_dictionary_tables as fetch_kegg
import fetch_extendedEntries as fetch_kegg_extended
import time
from datetime import datetime


def setDirectory():
    folder=get_timestamp();
    path=os.getcwd()+"/"+folder;
    if(os.path.isdir(path) == False):
        os.mkdir(folder)    
    os.chdir(path)
    
def get_timestamp():
    ts = time.time();
    st = datetime.fromtimestamp(ts).strftime('%Y%m%d');
    return st

def downloadDataFromKEGG():
    
    fetch_kegg.fetch_kegg_info();
    
    #download dictionary tables
    fetch_kegg.fetch_all_reactions();
    #fetch_kegg.fetch_all_metabolites();
    #fetch_kegg.fetch_all_organisms();
    #fetch_kegg.fetch_all_enzymes();
    #fetch_kegg.fetch_all_pathways()
    
    # download extended entries
    fetch_kegg_extended.fetch_reaction_entries();
    fetch_kegg_extended.fetch_organism_entries();
    fetch_kegg_extended.fetch_pathway_entries();
    

        
if __name__ == "__main__":
    
    setDirectory()
    
    print ("Start time:\t"+time.ctime()+"\n\n")
        
    #run
    downloadDataFromKEGG()
            
    print ("End time:\t"+time.ctime()+"\n\n")
    


