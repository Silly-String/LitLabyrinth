"""CSC111 Project 2: Applications of trees and graphs (Graphs Visualization)

Module Description
===============================

This Python module contains some functions for the visualization
of the graph for Project 2.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
import networkx as nx
from plotly.graph_objs import Scatter, Figure

import project2_part1

COLOUR_SCHEME = [
    '#2E91E5', '#E15F99', '#A71C80', '#FB0D0D', '#DA16FF', '#222A2A', '#1418F7',
    '#750D86', '#EB663B', '#511CFB', '#00A08B', '#FB00D1', '#FC0080', '#B2828D',
    '#5D327C', '#778AAE', '#862A16', '#A777F1', '#620042', '#1616A7', '#DA60CA',
    '#6C4516', '#0D2A63', '#AF0038'
]

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
BOOK_COLOUR = 'rgb(171, 71, 237)'
USER_COLOUR = 'rgb(91, 194, 245)'


def visualize_graph(graph: project2_part1.Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 5000,
                    output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """
    pos = getattr(nx, layout)(graph.to_networkx(max_vertices))

    kinds = [graph.to_networkx(max_vertices).nodes[k]['kind'] for k in graph.to_networkx(max_vertices).nodes]

    colours = [BOOK_COLOUR if kind == 'book' else USER_COLOUR for kind in kinds]

    x_edges = []
    y_edges = []
    for edge in graph.to_networkx(max_vertices).edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line={"color": LINE_COLOUR, "width": 1},
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=[pos[k][0] for k in graph.to_networkx(max_vertices).nodes],
                     y=[pos[j][1] for j in graph.to_networkx(max_vertices).nodes],
                     mode='markers',
                     name='nodes',
                     marker={"symbol": 'circle-dot', "size": 5, "color": colours,
                             "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}},
                     text=list(graph.to_networkx(max_vertices).nodes),
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    fig = Figure(data=[trace3, trace4])
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


def visualize_graph_clusters(graph: project2_part1.Graph, clusters: list[set],
                             layout: str = 'spring_layout',
                             max_vertices: int = 5000,
                             output_file: str = '') -> None:
    """Visualize the given graph, using different colours to illustrate the different clusters.

    Hides all edges that go from one cluster to another. (This helps the graph layout algorithm
    positions vertices in the same cluster close together.)

    Same optional arguments as visualize_graph (see that function for details).
    """
    graph_nx = graph.to_networkx(max_vertices)
    for edge in list(graph_nx.edges):
        # Check if edge is within the same cluster
        if any((edge[0] in cluster) != (edge[1] in cluster) for cluster in clusters):
            graph_nx.remove_edge(edge[0], edge[1])

    pos = getattr(nx, layout)(graph_nx)

    colors = []
    for k in graph_nx.nodes:
        for i, c in enumerate(clusters):
            if k in c:
                colors.append(COLOUR_SCHEME[i % len(COLOUR_SCHEME)])
                break
        else:
            colors.append(BOOK_COLOUR)

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # trace3 = Scatter(x=x_edges,
    #                  y=y_edges,
    #                  mode='lines',
    #                  name='edges',
    #                  line={"color": LINE_COLOUR, "width": 1},
    #                  hoverinfo='none'
    #                  )
    # trace4 = Scatter(x=[pos[index][0] for index in graph_nx.nodes],
    #                  y=[pos[j][1] for j in graph_nx.nodes],
    #                  mode='markers',
    #                  name='nodes',
    #                  marker={"symbol": 'circle-dot', "size": 5, "color": colors,
    #                          "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}},
    #                  text=list(graph_nx.nodes),
    #                  hovertemplate='%{text}',
    #                  hoverlabel={'namelength': 0}
    #                  )

    fig = Figure(data=[Scatter(x=x_edges,
                               y=y_edges,
                               mode='lines',
                               name='edges',
                               line={"color": LINE_COLOUR, "width": 1},
                               hoverinfo='none'),
                       Scatter(x=[pos[index][0] for index in graph_nx.nodes],
                               y=[pos[j][1] for j in graph_nx.nodes],
                               mode='markers',
                               name='nodes',
                               marker={"symbol": 'circle-dot', "size": 5, "color": colors,
                                       "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}},
                               text=list(graph_nx.nodes),
                               hovertemplate='%{text}',
                               hoverlabel={'namelength': 0}
                               )])
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.show()

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx', 'project2_part1', 'plotly.graph_objs'],
        'max-line-length': 120,
    })
