import plotly.graph_objects as go


def empty_figure(label_annotation):
    '''
    Returns an empty plot with a centered text.
    '''

    trace1 = go.Scatter(
        x=[],
        y=[]
    )

    data = [trace1]

    layout = go.Layout(
        showlegend=False,
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        annotations=[
            dict(
                x=0,
                y=0,
                xref='x',
                yref='y',
                text=label_annotation,
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=0
            )
        ]
    )

    fig = go.Figure(data=data, layout=layout)
    # END
    return fig
