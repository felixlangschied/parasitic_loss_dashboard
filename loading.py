import ipywidgets as widgets


def generate_widgets():
    core_factor = widgets.FloatSlider(
        value=0.9,
        min=0,
        max=1.0,
        step=0.1,
        description='Core factor:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
    )

    loss_factor = widgets.FloatSlider(
        value=0.6,
        min=0,
        max=1.0,
        step=0.1,
        description='Loss factor',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
    )


    propagate_annotation = widgets.Dropdown(
        options=['full', 'first'],
        value='first',
        description='Annotation:',
        disabled=False,
    )
    return core_factor, loss_factor, propagate_annotation


def get_parasets(taxadf):
    
    nonparasitic = taxadf.shortname[taxadf.parasitism == 'non'].to_list()
    parasitic = taxadf.shortname[taxadf.parasitism != 'non'].to_list()
    holoparasites = taxadf.shortname[taxadf.parasitism == 'holo'].to_list()
    hemiparasites = taxadf.shortname[taxadf.parasitism == 'hemi'].to_list()

    return nonparasitic, parasitic, holoparasites, hemiparasites