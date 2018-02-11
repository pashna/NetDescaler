import pandas as pd
import numpy as np
import networkx as nx
import numpy
import matplotlib.pyplot as plt

class GraphVisualizer:

    def __init__(self):
        pass

    def draw_graph(self, links, hosts=[]):
        from_nodes = []
        to_nodes = []

        print(hosts)

        for l in links:
            print(l)
            from_nodes.append(l['node1'])
            to_nodes.append(l['node2'])

        nodes = np.unique(from_nodes + to_nodes)
        types = []

        hosts = set(hosts)
        for n in nodes:

            if n in hosts:
                types.append(1)
            else:
                types.append(0)

        df = pd.DataFrame({'from': from_nodes, 'to': to_nodes})
        carac = pd.DataFrame({'ID': nodes, 'types': types})
        nx.Graph()
        G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())
        G.nodes()
        carac = carac.set_index('ID')
        carac = carac.reindex(G.nodes())
        print(types)
        carac['types'] = pd.Categorical(carac['types'])
        carac['types'].cat.codes
        nx.draw(G, with_labels=True, node_color=carac['types'].cat.codes, cmap=plt.cm.Set1, node_size=1500)
        plt.show()
        return