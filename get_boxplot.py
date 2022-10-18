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

    real_or_synth = 'real'

    if real_or_synth == 'synthetic':
        source_path = '/oak/stanford/groups/ogevaert/data/Patho-RNA-GAN/hover_net/synthetic/'
    else:
        source_path = '/oak/stanford/groups/ogevaert/data/Prad-TCGA/hover_net_synth/'

    projects = ['CESC', 'COAD', 'ESCA', 'GBM', 'KIRP', 'LUAD', 'PAAD']#np.unique([i[5:].split('_')[0] for i in tiles])

    for project in projects:
        print(project)
        tiles = os.listdir(source_path)
        tiles = [i for i in tiles if (project in i)]
        amt_no_cells = 0 #amt of tiles where no cells were detected

        for tile in tqdm(tiles):

            path = source_path+tile+'/json'
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

        my_colors = ["#FD2C52", "#8DE5A1", "#7B94FE", "#FED72B", "#FEBB7C"]
        sns.set_palette( my_colors )

        # plotting box plot
        ax = sns.boxplot(data=fractions_df, showfliers=False)
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
        for patch in ax.artists:
            r, g, b, a = patch.get_facecolor()
            patch.set_facecolor((r, g, b, .3))

        # plotting swarn plot on top of box plot
        sns.stripplot(data=fractions_df, size=1) #color=".25", 

        print('No cells detected in '+str(amt_no_cells)+' tiles, of total of '+str(len(tiles)))
        #plt.title('')
        plt.ylim([-0.025,1])
        plt.ylabel('Fraction')
        #plt.xlabel('Cell type')
        plt.savefig('/oak/stanford/groups/ogevaert/code/hover_net/boxplots/'+real_or_synth+'/'+project+'-'+real_or_synth+'.png',dpi=300)
        plt.clf()
        
