import json
import networkx as nx
import matplotlib.pyplot as plt

BIG_NUMBER = 1e10

def main():
	filename = "instances/toy_instance.json"
	#filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)

	# test file reading

	nodos_retiro = []
	nodos_tigre = []
	ids = list(data["services"].keys())
	u = data["rs_info"]["max_rs"]
	capacidad_vagon = data["rs_info"]["capacity"]
	G = nx.DiGraph()

	for i in range(len(ids)):
		origen = data["services"][ids[i]]["stops"][0]
		destino = data["services"][ids[i]]["stops"][1]

		l = data["services"][ids[i]]["demand"][0] / capacidad_vagon #cota inferior para cada servicio

		if (origen["station"] == "Retiro" and destino["station"] == "Tigre"):
			G.add_node(origen["time"], bipartite=0, demand=l)
			G.add_node(destino["time"], bipartite=1, demand=-l)
			nodos_retiro.append(origen["time"])
			nodos_tigre.append(destino["time"])
		else:
			G.add_node(origen["time"], bipartite=1, demand=l)
			G.add_node(destino["time"], bipartite=0, demand=-l)
			nodos_retiro.append(destino["time"])
			nodos_tigre.append(origen["time"])
		
		G.add_edge(origen["time"], destino["time"], capacity=u-l, weight=0)
		
	nodos_retiro = sorted(set(nodos_retiro)) #ordena y elimina duplicados
	nodos_tigre = sorted(set(nodos_tigre))

	for i in range(len(nodos_retiro) - 1):
		G.add_edge(nodos_retiro[i], nodos_retiro[i+1], capacity=BIG_NUMBER, weight=0)
	
	for i in range(len(nodos_tigre) - 1):
		G.add_edge(nodos_tigre[i], nodos_tigre[i+1], capacity=BIG_NUMBER, weight=0)

	if nodos_retiro:
		G.add_edge(nodos_retiro[-1], nodos_retiro[0], capacity=BIG_NUMBER, weight=1)
	if nodos_tigre:
		G.add_edge(nodos_tigre[-1], nodos_tigre[0], capacity=BIG_NUMBER, weight=1)

	min_flow_cost= nx.min_cost_flow(G)
	min_cost= nx.cost_of_flow(G, min_flow_cost)
	flujo_total = 0
	for u, v in G.edges():
		flujo = min_flow_cost[u][v]
		flujo_total += flujo
		print(f"Flujo de {u} a {v}: {flujo}")
	print("Flujo de costo mínimo:", min_cost)
	print("Flujo aristas:", min_flow_cost)
	#print("Nodos del grafo:", G.nodes(data=True))
	#print("Aristas del grafo:", G.edges(data=True))

if __name__ == "__main__":
	main()