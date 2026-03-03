import json
import networkx as nx
import math

def main():
    filename = "instances/retiro-tigre/retiro_tigre_semana.json"

    with open(filename) as json_file:
        data = json.load(json_file)

    #guardamos los nombres de las estaciones del servicio
    estacion_origen = data["stations"][0]
    estacion_destino = data["stations"][1]
    
    G = nx.DiGraph() #creamos grafo para representar el servicio
    ids = list(data["services"].keys()) #obtenemos los ids de los servicios
    capacidad_vagon = data["rs_info"]["capacity"] #guardamos la capacidad de los vagones
    u = data["rs_info"]["max_rs"] #guardamos la cantidad maxima de vagones que puede mandar el servicio
    nodos_origen = []
    nodos_destino = []

    for i in range(len(ids)):
        #para cada viaje, guardamos los el origen, el tiempo de salida, la estacion de salida, el destino, el tiempo de llegada y la estacion de llegada
        nodo_origen = data["services"][ids[i]]["stops"][0]
        nodo_origen_time = nodo_origen["time"]
        nodo_origen_station = nodo_origen["station"]

        nodo_destino = data["services"][ids[i]]["stops"][1]
        nodo_destino_time = nodo_destino["time"]
        nodo_destino_station = nodo_destino["station"]

        l = math.ceil(data["services"][ids[i]]["demand"][0]/capacidad_vagon) #calculamos la cantidad de vagones necesarios, redondeando hacia arriba
        G.add_node(f"{nodo_origen_time}_{nodo_origen_station}", time = nodo_origen_time, station = nodo_origen_station, demanda = l) #creamos el nodo para el origen
        G.add_node(f"{nodo_destino_time}_{nodo_destino_station}", time = nodo_destino_time, station = nodo_destino_station, demanda = -l) #creamos el nodo para el destino

        G.add_edge(f"{nodo_origen_time}_{nodo_origen_station}", f"{nodo_destino_time}_{nodo_destino_station}", capacidad = u-l, costo = 0, tipo = "tren") #creamos la arista entre el origen y el destino

    for nodo in G.nodes():
        #guardamos los tiempos de cada estacion en una lista
        if G.nodes[nodo]["station"] == estacion_origen:
            nodos_origen.append(G.nodes[nodo]["time"])
        else:
            nodos_destino.append(G.nodes[nodo]["time"])

    #hacemos la lista un set para eliminar los duplicados y la ordenamos para poder agregar las aristas de traspaso y las de trasnoche
    nodos_origen = sorted(set(nodos_origen))
    nodos_destino = sorted(set(nodos_destino))

    #agregamos las aristas de traspaso entre los nodos de la misma estacion
    for i in range(len(nodos_origen) - 1):
        G.add_edge(f"{nodos_origen[i]}_{estacion_origen}", f"{nodos_origen[i+1]}_{estacion_origen}", capacidad = float('inf'), costo = 0, tipo="traspaso")
    for i in range(len(nodos_destino) - 1):
        G.add_edge(f"{nodos_destino[i]}_{estacion_destino}", f"{nodos_destino[i+1]}_{estacion_destino}", capacidad = float('inf'), costo = 0, tipo = "traspaso")
    
    #agregamos las aristas de trasnoche entre el ultimo nodo y el primero de cada estacion
    G.add_edge(f"{nodos_origen[-1]}_{estacion_origen}", f"{nodos_origen[0]}_{estacion_origen}", capacidad = float('inf'), costo = 1 , tipo = "trasnoche")
    G.add_edge(f"{nodos_destino[-1]}_{estacion_destino}", f"{nodos_destino[0]}_{estacion_destino}", capacidad = float('inf'), costo = 1, tipo = "trasnoche")

    #calculamos el flujo minimo
    min_flow_cost = nx.min_cost_flow(G,"demanda", "capacidad", "costo")

    for u, v in G.edges:
        #para las aristas de tipo tren, le agregamos la demanda al flujo minimo
        if G.edges[u,v]["tipo"] == "tren":
            min_flow_cost[u][v] += G.nodes[u]["demanda"]
        if G.edges[u,v]["tipo"] == "trasnoche" and G.nodes[u]["station"] == estacion_origen:
            vagones_necesarios_origen = min_flow_cost[u][v] #el flujo en las aristas de trasnoche es la cantidad de vagones necesarios en esa estación
        if G.edges[u,v]["tipo"] == "trasnoche" and G.nodes[u]["station"] == estacion_destino:
            vagones_necesarios_destino = min_flow_cost[u][v]  #el flujo en las aristas de trasnoche es la cantidad de vagones necesarios en esa estación
        print("Cantidad de vagones de ", u, " a ", v, ": ", min_flow_cost[u][v])

    min_cost = nx.cost_of_flow(G, min_flow_cost, "costo") #el costo minimo nos indica la cantidad total de vagones necesarios
    print(f"La cantidad total de vagones necesarios son {min_cost}: {vagones_necesarios_origen} en {estacion_origen} y {vagones_necesarios_destino} en {estacion_destino}")
    print("Costo minimo: ", min_cost)


if __name__ == "__main__":
	main()
