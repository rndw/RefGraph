
### plotly the graph
#G = nx.random_geometric_graph(200, 0.125)
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pandas as pd

#edge_x = []
#edge_y = []
#for edge in g.edges():
#    x0, y0 = g.node[edge[0]]['pos']
#    x1, y1 = g.node[edge[1]]['pos']
#    edge_x.append(x0)
#    edge_x.append(x1)
#    edge_x.append(None)
#    edge_y.append(y0)
#    edge_y.append(y1)
#    edge_y.append(None)

#custom setup


#edge_trace = go.Scatter(
#    x=edge_xc, y=edge_yc,
#    line=dict(width=0.5, color='#888'),
#    hoverinfo='none',
#    mode='lines')


############alternative path
#custom setup


#edge_tracey = go.Scatter(
#    x=edge_xcy, y=edge_ycy,
#    line=dict(width=2, color='#200'),
#    hoverinfo='none',
#    mode='lines')

#node_x = []
#node_y = []
#for node in g.nodes():
#    x, y = g.node[node]['pos']
#    node_x.append(x)
#    node_y.append(y)





#### coloring ### not my function
node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(g.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text


### custom
edge_xc = []
edge_xc = [1,2,None,2,3,None,1,3,None]
edge_yc = []
edge_yc = [1,2,None,2,1,None,1,1,None]

edge_xcy = []
edge_xcy = [1,2,None]
edge_ycy = []
edge_ycy = [1,2,None]

node_xc = []
node_xc = [1,2,3]
node_yc = []
node_yc = [1,2,1]


fig = go.Figure()

# Add scatter trace for line
fig.add_trace(go.Scatter(
    x=edge_xcy, y=edge_ycy,
    line=dict(width=2, color='#200'),
    hoverinfo='none',
    mode='lines'))
fig.add_trace(go.Scatter(
    x=edge_xc, y=edge_yc,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'))
fig.add_trace(go.Scatter(
    x=node_xc, y=node_yc,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2)))

fig.layout.update(
    shapes=[
        # 1st highlight during Feb 4 - Feb 6
        go.layout.Shape(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0=0.75,
            y0=0.75,
            x1=1.25,
            y1=1.25,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
    ]
)

plot(fig)