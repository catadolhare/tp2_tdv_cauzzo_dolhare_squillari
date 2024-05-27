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

	nx.draw(G, with_labels=True, font_weight='bold')
	plt.show()

if __name__ == "__main__":
	main()