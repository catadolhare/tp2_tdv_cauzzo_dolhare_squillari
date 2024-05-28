import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
	filename = "instances/toy_instance.json"
	#filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)

	# test file reading

	G = nx.DiGraph()

	for service in data["services"]:
		print(service, data["services"][service]["stops"])
		for stop in data["services"][service]["stops"]:
			if stop["station"] == "Retiro":
				G.add_node((stop["time"], stop["type"]), bipartite=0)
			if stop["station"] == "Tigre":
				G.add_node((stop["time"], stop["type"]), bipartite=1)

	nodos_retiro = [node for node in G.nodes() if G.nodes[node]['bipartite'] == 0]
	nodos_tigre = [node for node in G.nodes() if G.nodes[node]['bipartite'] == 1]
	node_colors = ['#7878ff' if node[1] == 'D' else '#ff5757' for node in G.nodes()]
	edges_colors = ['blue' if node[1] == 'D' else 'red' for node in G.nodes()]
	node_labels = {node: f"{node[0]}" for node in G.nodes()}

	pos = nx.bipartite_layout(G, nodes=nodos_retiro)

	nx.draw(G, pos, with_labels=True, font_weight='bold', node_color =  node_colors, node_shape='s', node_size=700, edge_color=edges_colors, labels = node_labels)
	print(G.nodes)
	
	plt.show()

if __name__ == "__main__":
	main()