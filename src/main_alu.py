import json
import networkx as nx
import math

def main():
    '''
    print("Seleccione un viaje:")
    print("1. Retiro - Tigre")
    print("2. Villa Ballester - Zarate")
    print("3. Victoria - Los Cardales")
    print("4. Moreno - Mercedes")
    input_viaje = input()'''
    estacion_origen = ""
    estacion_destino = ""
    '''
    if input_viaje == "1":
        filename = "instances/retiro-tigre-semana.json"
        estacion_origen = "Retiro"
        estacion_destino = "Tigre"
    elif input_viaje == "2":
        filename = "instances/villa-ballester-zarate-semana.json"
        estacion_origen = "Villa Ballester"
        estacion_destino = "Zarate"
    elif input_viaje == "3":
        filename = "instances/victoria-los-cardales-semana.json"
        estacion_origen = "Victoria"
        estacion_destino = "Los Cardales"
    elif input_viaje == "4":
        filename = "instances/moreno_mercedes.json"
        estacion_origen = "Moreno"
        estacion_destino = "Mercedes"'''
    
    filename = "instances/poco_villa_ballester_mucho_zarate.json"
    estacion_origen = "Villa Ballester"
    estacion_destino = "Zarate"

    with open(filename) as json_file:
        data = json.load(json_file)
    
    G = nx.DiGraph() #creamos grafo para representar el servicio
    ids = list(data["services"].keys()) #obtenemos los ids de los servicios
    capacidad_vagon = data["rs_info"]["capacity"] #guardamos la capacidad de los vagones
    u = data["rs_info"]["max_rs"] #guardamos la cantidad maxima de vagones que puede mandar el servicio
    nodos_origen = []
    nodos_destino = []

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
        if G.nodes[nodo]["station"] == estacion_origen:
            nodos_origen.append(G.nodes[nodo]["time"])
        else:
            nodos_destino.append(G.nodes[nodo]["time"])

    nodos_origen = sorted(set(nodos_origen))
    nodos_destino = sorted(set(nodos_destino))

    for i in range(len(nodos_origen) - 1):
        G.add_edge(f"{nodos_origen[i]}_{estacion_origen}", f"{nodos_origen[i+1]}_{estacion_origen}", capacidad = float('inf'), costo = 0, tipo="traspaso")
    for i in range(len(nodos_destino) - 1):
        G.add_edge(f"{nodos_destino[i]}_{estacion_destino}", f"{nodos_destino[i+1]}_{estacion_destino}", capacidad = float('inf'), costo = 0, tipo = "traspaso")
    
    G.add_edge(f"{nodos_origen[-1]}_{estacion_origen}", f"{nodos_origen[0]}_{estacion_origen}", capacidad = float('inf'), costo = 1 , tipo = "trasnoche")
    G.add_edge(f"{nodos_destino[-1]}_{estacion_destino}", f"{nodos_destino[0]}_{estacion_destino}", capacidad = float('inf'), costo = 1, tipo = "trasnoche")

    min_flow_cost = nx.min_cost_flow(G,"demanda", "capacidad", "costo")

    for u, v in G.edges:
        if G.edges[u,v]["tipo"] == "tren":
            min_flow_cost[u][v] += G.nodes[u]["demanda"]
        if G.edges[u,v]["tipo"] == "trasnoche" and G.nodes[u]["station"] == estacion_origen:
            vagones_necesarios_origen = min_flow_cost[u][v]
        if G.edges[u,v]["tipo"] == "trasnoche" and G.nodes[u]["station"] == estacion_destino:
            vagones_necesarios_destino = min_flow_cost[u][v]
        print("Cantidad de vagones de ", u, " a ", v, ": ", min_flow_cost[u][v])

    min_cost = nx.cost_of_flow(G, min_flow_cost, "costo")
    print(f"La cantidad total de vagones necesarios son {vagones_necesarios_origen + vagones_necesarios_destino}: {vagones_necesarios_origen} en {estacion_origen} y {vagones_necesarios_destino} en {estacion_destino}")
    print("Costo minimo: ", min_cost)


if __name__ == "__main__":
	main()