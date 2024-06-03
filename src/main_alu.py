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

	servicios_retiro = []
	servicios_tigre = []
	nodos_retiro = []
	nodos_tigre = []
	ids = list(data["services"].keys())
	u = data["rs_info"]["max_rs"]
	capacidad_vagon = data["rs_info"]["capacity"]
	aristas_servicios = []
	imbalance = {}

	for i in range(len(ids)):
		origen = data["services"][ids[i]]["stops"][0]
		destino = data["services"][ids[i]]["stops"][1]

		if (origen["station"] == "Retiro" and destino["station"] == "Tigre"):
			servicios_retiro.append((i+1, origen["time"], origen["type"], data["services"][ids[i]]["demand"]))
			servicios_tigre.append((i+1, destino["time"], destino["type"], data["services"][ids[i]]["demand"]))
			nodos_retiro.append(origen["time"]) #ver lo del dos horarios iguales en diferentes estaciones
			nodos_tigre.append(destino["time"])
		else:
			servicios_tigre.append((i+1, origen["time"], origen["type"], data["services"][ids[i]]["demand"]))
			servicios_retiro.append((i+1, destino["time"], destino["type"], data["services"][ids[i]]["demand"]))
			nodos_retiro.append(destino["time"])
			nodos_tigre.append(origen["time"])
	
		l = data["services"][ids[i]]["demand"][0] / capacidad_vagon #cota inferior para cada servicio
		arista = (origen["time"], destino["time"], {'capacity': u, 'weigth': 0, 'demand': l})
		aristas_servicios.append(arista)
	'''
		if origen["time"] not in imbalance:
			imbalance[origen["time"]] = 0
		if destino["time"] not in imbalance:
			imbalance[destino["time"]] = 0
		imbalance[origen["time"]] += l
		imbalance[destino["time"]] -= l
	'''
	for i in range(len(nodos_retiro)):
		if nodos_retiro[i] not in imbalance:
			imbalance[nodos_retiro[i]] = 0
	for i in range(len(nodos_tigre)):
		if nodos_tigre[i] not in imbalance:
			imbalance[nodos_tigre[i]] = 0
		

	nodos_retiro.sort()
	nodos_tigre.sort()
#arista derecha tiene que tener imbalance positivo y la izquierda negativo (si envio de A a B). 
#puedo enviar mas que el imbalance
#
	for i in range(len(nodos_retiro) - 1):
		arista = (nodos_retiro[i], nodos_retiro[i+1], {'capacity': BIG_NUMBER, 'weigth': 0, 'demand': 0})
		aristas_servicios.append(arista)
	
	for i in range(len(nodos_tigre) - 1):
		arista = (nodos_tigre[i], nodos_tigre[i+1], {'capacity': BIG_NUMBER, 'weigth': 0, 'demand': 0})
		aristas_servicios.append(arista)

	if nodos_retiro:
		aristas_servicios.append((nodos_retiro[-1], nodos_retiro[0], {'capacity': BIG_NUMBER, 'weigth': 1, 'demand': 0}))
	if nodos_tigre:
		aristas_servicios.append((nodos_tigre[-1], nodos_tigre[0], {'capacity': BIG_NUMBER, 'weigth': 1, 'demand': 0}))


	print("Retiro", servicios_retiro)
	print("Tigre", servicios_tigre)
	print("Nodos Retiro", nodos_retiro)
	print("Nodos Tigre", nodos_tigre)
	print("Aristas", aristas_servicios)

	G = nx.DiGraph()
	G.add_nodes_from(nodos_retiro, bipartite=0)
	G.add_nodes_from(nodos_tigre, bipartite=1)
	G.add_edges_from(aristas_servicios)

	for node, imbal in imbalance.items():
		G.nodes[node]['demand'] = imbal
	pos = nx.bipartite_layout(G, nodes=nodos_retiro)

	nx.draw(G, pos, with_labels=True, font_weight='bold')
	
	plt.show()

	min_flow_cost= nx.min_cost_flow(G)
	min_cost= nx.cost_of_flow(G, min_flow_cost)
	print("Flujo de costo mínimo:", min_cost)
	print("Flujo aristas:", min_flow_cost)

if __name__ == "__main__":
	main()