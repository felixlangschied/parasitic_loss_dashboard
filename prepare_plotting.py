import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist, squareform


def cluster_return_row_order(df):

    # 1. Compute pairwise distances between rows
    # For binary data, 'hamming' or 'jaccard' are good choices
    dist_matrix = pdist(df.values, metric="hamming")

    # 2. Perform hierarchical clustering
    linkage = sch.linkage(dist_matrix, method="average")  # or 'ward', 'single', etc.

    # 3. Get the order of rows from the dendrogram
    dendro = sch.dendrogram(linkage, no_plot=True)
    row_order = dendro['leaves']

    return row_order


def long_xlabels(taxadf, col_names):
    col = []
    for shortname in col_names:
        
        shortname = shortname.replace('.fa', '')
        longname = taxadf.name[taxadf.shortname == shortname].values[0]
        col.append(longname)
        # longname = taxadf.name[taxadf.shortname.replace('.fa', '') == shortname]
        # print(longname)
    return col    


def change_values_per_category(df, nonparasitic, hemiparasites, holoparasites):
    col = []
    col.append(df.copy().filter(nonparasitic).replace(1, 0))
    col.append(df.copy().filter(hemiparasites).replace(1.0, 0.5))   
    col.append(df.copy().filter(holoparasites))
    return pd.concat(col, axis=1)


def parse_protid2annotation_from_protein_faa(path):
    protid2annotation = {}
    with open(path) as fh:
        for line in fh:
            if not line.startswith('>'):
                continue
            protid = line.split()[0].replace('>', '')
            annotation = ' '.join(line.split('[')[0].split()[1:])
            protid2annotation[protid] = annotation
    return protid2annotation
    

def generate_Athaliana_annotation_df(df, ath_protid2annotation, mode):
    """
    mode: "full"/"first"/"longest" -> add annotation string for each coortholog in Athaliana, or just add the first one
    """
    col = []
    index2annotations = {}
    for i, row in df.iterrows():
        protids = row['Athaliana']
        annotations = []
        for protid in protids.split(','):
            if protid in ath_protid2annotation:
                annotations.append(ath_protid2annotation[protid])
            else:
                annotations.append('None')
        # index2annotations[i] = '; '.join(annotations)
        if mode == "full":
            annostring = '; '.join(annotations)
        elif mode == "first":
            annostring = annotations[0]
        else:
            raise ValueError(f'Unknown mode "{mode}". choose between "first" and "full"')
            
            
        col.append(['Ath: ' + annostring] * df.columns.size)
    return pd.DataFrame(col, columns=df.columns.values)
    
    
    

def prepare_for_heatmap(df, taxadf, ath_protid2annotation, mode, nonparasitic, hemiparasites, holoparasites):
    col_names = [f'{name}.fa' for name in nonparasitic + hemiparasites + holoparasites]
    df = df.loc[:,col_names]
    df = df.rename(columns={name: name.replace('.fa', '') for name in df.columns.values})

    xlabels = long_xlabels(taxadf, col_names)
    ylabels = [f'OG{i+1}' for i in df.index.to_list()]
    heatmap_df = df != "*"
    row_order = cluster_return_row_order(heatmap_df)
    heatmap_df = heatmap_df.iloc[row_order, :]
    heatmap_df = heatmap_df.astype(int).replace(0, None)
    heatmap_df = change_values_per_category(heatmap_df, nonparasitic, hemiparasites, holoparasites)

    
    label_df = df.iloc[row_order, :]
    anno_df = generate_Athaliana_annotation_df(label_df, ath_protid2annotation, mode)
    
    return heatmap_df, label_df, anno_df, xlabels, ylabels