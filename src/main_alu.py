import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
	filename = "instances/toy_instance.json"
	#filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)

	# test file reading

	servicios_retiro = []
	servicios_tigre = []
	nodos_retiro = []
	nodos_tigre = []
	ids = list(data["services"].keys())
	u = data["rs_info"]["max_rs"]
	capacidad_vagon = data["rs_info"]["capacity"]
	aristas_servicios = []

	for i in range(len(ids)):
		origen = data["services"][ids[i]]["stops"][0]
		destino = data["services"][ids[i]]["stops"][1]

		if (origen["station"] == "Retiro" and destino["station"] == "Tigre"):
			servicios_retiro.append((i+1, origen["time"], origen["type"], data["services"][ids[i]]["demand"]))
			servicios_tigre.append((i+1, destino["time"], destino["type"], data["services"][ids[i]]["demand"]))
			nodos_retiro.append(origen["time"])
			nodos_tigre.append(destino["time"])
		else:
			servicios_tigre.append((i+1, origen["time"], origen["type"], data["services"][ids[i]]["demand"]))
			servicios_retiro.append((i+1, destino["time"], destino["type"], data["services"][ids[i]]["demand"]))
			nodos_retiro.append(destino["time"])
			nodos_tigre.append(origen["time"])
	
		l = data["services"][ids[i]]["demand"][0] / capacidad_vagon #cota inferior para cada servicio
		arista = (origen["time"], destino["time"], {'capacity': u, 'cost': 0, 'demand': l})
		aristas_servicios.append(arista)

	nodos_retiro.sort()
	nodos_tigre.sort()

	for i in range(len(nodos_retiro) - 1):
		arista = (nodos_retiro[i], nodos_retiro[i+1], {'capacity': float('inf'), 'cost': 0, 'demand': 0})
		aristas_servicios.append(arista)
	
	for i in range(len(nodos_tigre) - 1):
		arista = (nodos_tigre[i], nodos_tigre[i+1], {'capacity': float('inf'), 'cost': 0, 'demand': 0})
		aristas_servicios.append(arista)

	if nodos_retiro:
		aristas_servicios.append((nodos_retiro[-1], nodos_retiro[0], {'capacity': float('inf'), 'cost': 1, 'demand': 0}))
	if nodos_tigre:
		aristas_servicios.append((nodos_tigre[-1], nodos_tigre[0], {'capacity': float('inf'), 'cost': 1, 'demand': 0}))


	print("Retiro", servicios_retiro)
	print("Tigre", servicios_tigre)
	print("Nodos Retiro", nodos_retiro)
	print("Nodos Tigre", nodos_tigre)
	print("Aristas", aristas_servicios)

	G = nx.DiGraph()
	G.add_nodes_from(nodos_retiro, bipartite=0)
	G.add_nodes_from(nodos_tigre, bipartite=1)
	G.add_edges_from(aristas_servicios)

	pos = nx.bipartite_layout(G, nodes=nodos_retiro)

	nx.draw(G, pos, with_labels=True, font_weight='bold')
	
	plt.show()
'''
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
	
	plt.show()'''

if __name__ == "__main__":
	main()