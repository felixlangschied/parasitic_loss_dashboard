import pandas as pd
pd.set_option('future.no_silent_downcasting', True)
import json
from dash import Dash, html, dash_table, dcc, callback, Output, Input

from src.loading import generate_widgets, get_parasets
from src.process_core import find_genes_lost_for_parasitism
from src.prepare_plotting import prepare_for_heatmap
from src.plotting import plot_loss_PP

# ---------------------------------------------------------------------------------------
# input paths
para_nonpara_overview = f'data/28taxa_overview.tsv'
og_path = f'data/28taxa_orthogroups.tsv'
ath_anno_path = 'data/ath_protid2annotation.json'

# load information about plants
taxadf = pd.read_csv(para_nonpara_overview, sep='\t')
nonparasitic, parasitic, holoparasites, hemiparasites = get_parasets(taxadf)
column_names = [f'{name}.fa' for name in hemiparasites + holoparasites]

# load orthology data
orthodf = pd.read_csv(og_path, sep='\t')

# load A thaliana annotations
with open(ath_anno_path) as fh:
    ath_protid2annotation = json.load(fh)


# ---------------------------------------------------------------------------------------
# Initialize the app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Phylogenetic tree of plant species", style={'fontFamily': 'Arial, sans-serif'}),
    html.Img(src='assets/28_parasiticplants_tree.png', alt='Phylogenetic tree', style={'width': '50%', 'height': 'auto'},),
    html.P([
        html.B('Figure:'), 
        ' Phylogenetic tree pruned from Zuntini et al. 2024, Nature.'
    ], style={'fontFamily': 'Arial, sans-serif'}),

    html.H1("\nGene Loss Heatmap Dashboard", style={'fontFamily': 'Arial, sans-serif'}),

    html.Div([
        html.Label("Presence in non-parasitic plants to be considered 'core'?"),
        dcc.Slider(
            0,
            1,
            0.1,
            id='core-factor-input',
            marks=None,
            tooltip={"placement": "bottom", "always_visible": False},
            value=0.9,

        ),
        html.Label("Absence in parasitic plants to be considered 'lost'?"),
        dcc.Slider(
            0,
            1,
            0.1,
            id='loss-factor-input',
            value=0.6,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": False},
        ),
        html.Label("Propagate A. thaliana annotation from first co-ortholog or from all?"),
        dcc.RadioItems(
            ['first', 'full'],
            'first',
            id='propagate',
        ),
    ], style={'width': '25%', 'margin': 'left', 'fontFamily': 'Arial, sans-serif'}),

    dcc.Graph(id='heatmap-graph'),
])

@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('core-factor-input', 'value'),
     Input('loss-factor-input', 'value'),
     Input('propagate', 'value')]
)
def update_heatmap(core_factor, loss_factor, propagate):
    # This is where your original loss_heatmap function's logic goes
    # with the input values from the dashboard.
    
    # 1. Process data based on new input factors
    loss_overview, lost_orthodf = find_genes_lost_for_parasitism(
        orthodf,
        nonparasitic,
        parasitic,
        column_names,
        core_factor=core_factor,
        loss_factor=loss_factor
    )

    # 2. Prepare data for plotting
    # propagate = 'first' # Assuming this is a fixed parameter
    heatmap_df, label_df, anno_df, xlabels, ylabels = prepare_for_heatmap(
        lost_orthodf, taxadf, ath_protid2annotation,
        propagate,
        nonparasitic,
        hemiparasites,
        holoparasites
    )

    # 3. Create the Plotly figure
    fig = plot_loss_PP(
        heatmap_df,
        xlabels,
        ylabels,
        label_df,
        anno_df
    )

    # 4. Return the figure to the dcc.Graph component
    return fig

if __name__ == '__main__':
    app.run(debug=True)

