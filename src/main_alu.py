import json
import networkx as nx
import math

BIG_NUMBER = 1e10

def main():
    #filename = "instances/toy_instance.json"
    filename = "instances/retiro-tigre-semana.json"
	
    with open(filename) as json_file:
        data = json.load(json_file)

	# test file reading
    
    G = nx.DiGraph()
    ids = ids = list(data["services"].keys())
    capacidad_vagon = data["rs_info"]["capacity"]
    u = data["rs_info"]["max_rs"]
    nodos_retiro = []
    nodos_tigre = []

    for i in range(len(ids)):
        nodo_origen = data["services"][ids[i]]["stops"][0]
        nodo_origen_time = nodo_origen["time"]
        nodo_origen_station = nodo_origen["station"]

        nodo_destino = data["services"][ids[i]]["stops"][1]
        nodo_destino_time = nodo_destino["time"]
        nodo_destino_station = nodo_destino["station"]

        l = math.ceil(data["services"][ids[i]]["demand"][0]/capacidad_vagon)

        G.add_node(f"{nodo_origen_time}_{nodo_origen_station}", time = nodo_origen_time, station = nodo_origen_station, demanda = l)
        G.add_node(f"{nodo_destino_time}_{nodo_destino_station}", time = nodo_destino_time, station = nodo_destino_station, demanda = -l)

        G.add_edge(f"{nodo_origen_time}_{nodo_origen_station}", f"{nodo_destino_time}_{nodo_destino_station}", capacidad = u-l, costo = 0, tipo = "tren")

    for nodo in G.nodes():
        if G.nodes[nodo]["station"] == "Retiro":
            nodos_retiro.append(G.nodes[nodo]["time"])
        else:
            nodos_tigre.append(G.nodes[nodo]["time"])

    nodos_retiro = sorted(set(nodos_retiro))
    nodos_tigre = sorted(set(nodos_tigre))

    for i in range(len(nodos_retiro) - 1):
        G.add_edge(f"{nodos_retiro[i]}_Retiro", f"{nodos_retiro[i+1]}_Retiro", capacidad = BIG_NUMBER, costo = 0, tipo="traspaso")
    for i in range(len(nodos_tigre) - 1):
        G.add_edge(f"{nodos_tigre[i]}_Tigre", f"{nodos_tigre[i+1]}_Tigre", capacidad = BIG_NUMBER, costo = 0, tipo = "traspaso")
    
    G.add_edge(f"{nodos_retiro[-1]}_Retiro", f"{nodos_retiro[0]}_Retiro", capacidad = BIG_NUMBER, costo = 1 , tipo = "trasnoche")
    G.add_edge(f"{nodos_tigre[-1]}_Tigre", f"{nodos_tigre[0]}_Tigre", capacidad = BIG_NUMBER, costo = 1, tipo = "trasnoche")

    min_flow_cost = nx.min_cost_flow(G,"demanda", "capacidad", "costo")

    for u, v in G.edges:
        if G.edges[u,v]["tipo"] == "tren":
            min_flow_cost[u][v] += G.nodes[u]["demanda"]
        if G.edges[u,v]["tipo"] == "trasnoche" and G.nodes[u]["station"] == "Retiro":
            vagones_necesarios_retiro = min_flow_cost[u][v]
        if G.edges[u,v]["tipo"] == "trasnoche" and G.nodes[u]["station"] == "Tigre":
            vagones_necesarios_tigre = min_flow_cost[u][v]
        print("Cantidad de vagones de ", u, " a ", v, ": ", min_flow_cost[u][v])

    min_cost = nx.cost_of_flow(G, min_flow_cost, "costo")
    print(f"La cantidad total de vagones necesarios son {min_cost}: {vagones_necesarios_retiro} en Retiro y {vagones_necesarios_tigre} en Tigre")
    print("Costo minimo: ", min_cost)


if __name__ == "__main__":
	main()