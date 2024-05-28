import json
import networkx as nx
import networkx as nx
import matplotlib.pyplot as plt

BIG_NUMBER = 1e10

def main():
	filename = "instances/toy_instance.json"
	#filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)
	
	####### OBTENGO LISTADO DE ID'S

	servicios_id = list(data["services"].keys())
	
	####### OBTENGO TIEMPO Y RECORRIDO ASOCIADOS A CADA ID

	servicios_tiempos_R = []
	servicios_tiempos_T = []
	servicios_extremos = []

	u = data["rs_info"]["max_rs"]
	capacidad_vagon = data["rs_info"]["capacity"]

	for i in range(len(servicios_id)):
		origen = data["services"][servicios_id[i]]["stops"][0]
		destino = data["services"][servicios_id[i]]["stops"][1]

		if (origen["station"] == "Retiro" and destino["station"] == "Tigre"):  #Agrego los tiempos a dos listas diferentes (Segun la estacion a la que correspondan) Para poder generar las aristas entre ellos
			servicios_tiempos_R.append(origen["time"])
			servicios_tiempos_T.append(destino["time"])
		
		else:
			servicios_tiempos_T.append(origen["time"])
			servicios_tiempos_R.append(destino["time"])

		l = data["services"][servicios_id[i]]["demand"][0] / capacidad_vagon  #Calculo el l para cada servicio

		arista = (origen["time"], destino["time"], {'U': u, 'C': 0, 'L': l}) #Tripla (Cant. máx. de vagones, costo, Cant. mín. de vagones)
		servicios_extremos.append(arista)
	
	servicios_tiempos_R.sort()  #Ordeno las listas para poder generar las aristas entre ellos
	servicios_tiempos_T.sort()
	servicios_tiempos = servicios_tiempos_R + servicios_tiempos_T

	for i in range(len(servicios_tiempos_R) - 1): #Genero aristas entre nodos en una misma estacion (azules)
		arista = (servicios_tiempos_R[i], servicios_tiempos_R[i+1], {'U': BIG_NUMBER, 'C': 0, 'L': 0})
		servicios_extremos.append(arista)
	
	for i in range(len(servicios_tiempos_T) - 1): #Genero aristas entre nodos en una misma estacion (azules)
		arista = (servicios_tiempos_T[i], servicios_tiempos_T[i+1], {'U': BIG_NUMBER, 'C': 0, 'L': 0})
		servicios_extremos.append(arista)

	#Genero aristas entre un día y el siguiente (rojas)
	arista = (servicios_tiempos_R[len(servicios_tiempos_R) - 1], servicios_tiempos_R[0], {'U': BIG_NUMBER, 'C': 1, 'L': 0})
	servicios_extremos.append(arista)

	arista = (servicios_tiempos_T[len(servicios_tiempos_T) - 1], servicios_tiempos_T[0], {'U': BIG_NUMBER, 'C': 1, 'L': 0})
	servicios_extremos.append(arista)

	print(servicios_tiempos)
	print(servicios_extremos)

	####### CREO DIGRAFO
	G = nx.DiGraph()
	G.add_nodes_from(servicios_tiempos) #Asigno como nodos los valores que almacené como tiempos
	G.add_weighted_edges_from(servicios_extremos) #Asigno como arcos los valores que almacené como recorrido de cada servicio

	######################## Todo esto es más para visualizar el grafo que otra cosa, CREO que no es tan necesario
	pos = {}
	for i, node in enumerate(servicios_tiempos):  #Hago que los nodos que corresponden a cada estacion se ubiquen de un lado del grafico
		if i < (len(servicios_tiempos) // 2):     
			pos[node] = (0, i)  
		else:
			pos[node] = (1, i - (len(servicios_tiempos) // 2))
	
	# Definir los colores para las aristas
	edge_colors = []
	total_edges = len(G.edges())
	edges = list(G.edges(data=True))

	for i, (u, v, data) in enumerate(edges):
		if i >= total_edges - 2:  # Las dos últimas aristas
			edge_colors.append('red')
		elif pos[u][0] != pos[v][0]:  # Cruzan de izquierda a derecha o de derecha a izquierda
			edge_colors.append('green')
		else:  # Se mueven dentro del lado izquierdo o derecho
			edge_colors.append('blue')

	# Dibujar el grafo con las posiciones y colores especificados
	nx.draw(G, pos, with_labels=True, node_color='gray', node_size=700, edge_color=edge_colors)
	labels = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
	plt.show()

	# test file reading

	#for service in data["services"]:
	#	print(service, data["services"][service]["stops"])

if __name__ == "__main__":
	main()