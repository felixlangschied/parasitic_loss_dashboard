from math import ceil
import matplotlib.pyplot as plt
import seaborn as sns


def filter_with_specnamelist(df, grouplist):
    return df.copy().filter([f'{shortname}.fa' for shortname in grouplist])


def find_core_indices(df, core_factor):
    minimum_orthologs = ceil(df.columns.size * core_factor)  # how many nonparasitic species need to have an ortholog to be considered core?
    mask = df.sum(axis=1) >= minimum_orthologs
    return df.index[mask].tolist()


def count_and_plot_geneloss(df):
    sns.set(rc={'figure.figsize':(6,4), 'ytick.left': False, 'xtick.bottom': False}, font_scale = 1, style='whitegrid')
    gene_loss = df.columns.size - df.sum(axis=1)
    sns.histplot(gene_loss, discrete=True)
    plt.title(f'Number of non-parasitic core genes: {gene_loss.index.size}')
    plt.xticks(range(0,gene_loss.max() + 1))
    plt.xlabel('Non-parasitic core genes lost in X parasitic plants')
    
    
def find_lost_core_genes(df, loss_factor):
    return df[df.columns.size - df.sum(axis=1) >= 10 * loss_factor]


###########################################################################################################################

def find_genes_lost_for_parasitism(inputdf, nonparasitic, parasitic_subtype, column_names, core_factor, loss_factor):

    
    ## START
    df = inputdf.copy().filter([column for column in inputdf.columns if column.endswith('.fa')])
    # Turn every cell without an ortholog to False
    df_bool = df != "*"
    # find rows that are True in nonparasitic but false in parasitic

    non_parasitic_df = filter_with_specnamelist(df_bool, nonparasitic)
    non_parasitic_core_indices = find_core_indices(non_parasitic_df, core_factor)
    
    parasitic_orthologs_nonparasitic_core = filter_with_specnamelist(df_bool, parasitic_subtype).loc[non_parasitic_core_indices, :]
    
    # display(parasitic_orthologs_nonparasitic_core)
    # count_and_plot_geneloss(parasitic_orthologs_nonparasitic_core)
    lost_core_genes = find_lost_core_genes(parasitic_orthologs_nonparasitic_core, loss_factor)
    # sns.heatmap(lost_core_genes)
    # display(lost_core_genes)
    
    # map back to orthoids
    lost_orthodf = inputdf.loc[lost_core_genes.index, :]
    return lost_core_genes, lost_orthodf
