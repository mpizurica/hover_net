import pandas as pd
import os 
from tqdm import tqdm
import numpy as np
from collections import Counter

def get_type(row):
    nuc = row['nuc']
    return nuc['type']

if __name__=='__main__':

    type_info = {
            0 : "no label",
            1 : "Tumor cells",
            2 : "Lymphocytes",
            3 : "Connective Tissue", 
            4 : "Dead Cells", 
            5 : "Normal Epithelial", 
        }

    source_path = '/oak/stanford/groups/ogevaert/data/Patho-RNA-GAN/hover_net/synthetic/'
    output_filename = 'cell_counts_synth.txt'

    files = os.listdir(source_path)

    try:
        done = pd.read_csv(output_filename,  header=0, delim_whitespace=True)
        already_written = done['file'].values
    except:
        done = None
        already_written = []

    files_ = [i for i in files if i not in already_written]
    
    for file in tqdm(files_):

        all_counts_list = {
            "no label" : 0,
            "Tumor cells" : 0,
            "Lymphocytes" : 0,
            "Connective Tissue" : 0,
            "Dead Cells" : 0,
            "Normal Epithelial" : 0
        }

        path = source_path+file+'/json'

        json_file = file + '.json'

        try:
        
            df = pd.read_json(path+'/'+json_file)
            types = df.apply(lambda row: get_type(row), axis=1)

            if types.shape[0] > 0:
                types_str = [type_info[i] for i in types]
                counts = Counter(types_str)

                for k in all_counts_list.keys():
                    all_counts_list[k] += counts[k]

            counts_df = pd.DataFrame(all_counts_list, index=[file,])
            
            with open(output_filename, 'a') as f:
                dfAsString = counts_df.to_string(header=False, index=True)
                f.write('\n')
                f.write(dfAsString)

        except:
            print('bad json file '+file)
        