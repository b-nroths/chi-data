import matplotlib
matplotlib.use('Agg')
import osmnx as ox

G = ox.graph_from_place('Manhattan Island, New York City, New York, USA', network_type='drive')
ox.plot_graph(ox.project_graph(G))