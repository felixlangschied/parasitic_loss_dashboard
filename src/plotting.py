import plotly.express as px
import plotly.graph_objects as go


def plot_loss_PP(heatmap_df, xlabels, ylabels, label_df, anno_df):
    custom_colorscale = [
        [0, '#999999'],
        [0.5, '#f1c232'],
        [1, '#cc0000']
    ]

    fig = go.Figure(data=go.Heatmap(
                        z=heatmap_df,
                        x=xlabels,
                        y=ylabels,
                        text=label_df,
                        customdata=anno_df,
                        hoverinfo='x+text',
                        hoverongaps=False,
                        showscale=False,
                        type='heatmap',
                        colorscale=custom_colorscale,
                        hovertemplate=
                        "<b>%{x}</b><br>" +
                        "%{customdata}<br>" +
                        "%{text}<br><br>" +
                        "<extra></extra>",
    ))

    # Change layout
    row_height = 20
    height = max(400, row_height * heatmap_df.index.size)
    fig.update_layout(
        width=800,
        height=height,
        title=f'Number of Orthologous groups: {heatmap_df.index.size}'
    )

    # Add vertical and horizontal grid lines as shapes
    n_rows, n_cols = heatmap_df.shape
    shapes = []

    # Vertical lines (between columns)
    for i in range(1, n_cols):
        shapes.append(dict(
            type="line",
            x0=i-0.5, x1=i-0.5,
            y0=-0.5, y1=n_rows-0.5,
            line=dict(color="white", width=1)
        ))

    # Horizontal lines (between rows)
    for j in range(1, n_rows):
        shapes.append(dict(
            type="line",
            x0=-0.5, x1=n_cols-0.5,
            y0=j-0.5, y1=j-0.5,
            line=dict(color="white", width=1)
        ))

    fig.update_layout(
        shapes=shapes,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, autorange="reversed")  # reverse so row0 is at top
    )

    return fig

