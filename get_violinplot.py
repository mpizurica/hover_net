import pandas as pd 
import numpy as np
from collections import Counter
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import numpy as np

def get_type(row):
    nuc = row['nuc']
    return nuc['type']

if __name__ == "__main__":
    sns.set()
    sns.set_style({'axes.grid' : False})
    my_colors = ["#FD2C52", "#8DE5A1", "#7B94FE", "#FED72B", "#FEBB7C"]
    sns.set_palette( my_colors )

    type_info = {
        0 : "no label",
        1 : "Tumor cells",
        2 : "Lymphocytes",
        3 : "Connective Tissue", 
        4 : "Dead Cells", 
        5 : "Normal Epithelial", 
    }

    all_counts_list = {
        "no label" : [],
        "Tumor cells" : [],
        "Lymphocytes" : [],
        "Connective Tissue" : [],
        "Dead Cells" : [],
        "Normal Epithelial" : []
    }

    
    source_path_real = '/oak/stanford/groups/ogevaert/data/Patho-RNA-GAN/hover_net/synthetic/'
    source_path_synth = '/oak/stanford/groups/ogevaert/data/Prad-TCGA/hover_net_synth/'
    sources = [source_path_real, source_path_synth]

    projects = ['CESC', 'COAD', 'ESCA', 'GBM', 'KIRP', 'LUAD', 'PAAD']#np.unique([i[5:].split('_')[0] for i in tiles])

    for project in projects:

        print(project)
        tiles_real = [i for i in os.listdir(source_path_real) if (project in i)] 
        tiles_synth = [i for i in os.listdir(source_path_synth) if (project in i)]  

        dfs = [] # add fractions_df real and synth here
        tiles_all = [tiles_real, tiles_synth]

        for i, tiles in enumerate(tiles_all):
            amt_no_cells = 0

            for tile in tqdm(tiles):
                path = sources[i]+tile+'/json'
                json_file = tile+'.json'
                
                try:
                    df = pd.read_json(path+'/'+json_file)
                    types = df.apply(lambda row: get_type(row), axis=1)
            
                    types_str = [type_info[i] for i in types]
                    counts = Counter(types_str)

                    for k in all_counts_list.keys():
                        all_counts_list[k].append(round(counts[k]/sum(counts.values()),3))
                except:
                    #print('No cells found for '+json_file)
                    amt_no_cells+=1

            fractions_df = pd.DataFrame(all_counts_list)
            fractions_df = fractions_df.drop(columns={'no label'})

            if i == 0:
                type = 'real'
            else:
                type = 'synth'

            fractions_df['type'] = type
            dfs.append(fractions_df)
            print('No cells detected in '+str(amt_no_cells)+' tiles, of total of '+str(len(tiles)))

        total_df = pd.concat(dfs)
        temp = pd.melt(total_df, value_vars=['Tumor cells',  'Lymphocytes',  'Connective Tissue',  'Dead Cells',  'Normal Epithelial'], id_vars='type')
        ax = sns.violinplot(x='variable', y='value', hue='type', data=temp)
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)

        plt.ylim([-0.025,1])
        plt.savefig('/oak/stanford/groups/ogevaert/code/hover_net/violins/'+project+'.png')
        plt.clf()
            

            
