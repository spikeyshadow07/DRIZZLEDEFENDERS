import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time
import random

# Load graph
graph = ox.load_graphml("city_graph.graphml")

# Generate a valid route (safe method)
while True:
    start = random.choice(list(graph.nodes))
    end = random.choice(list(graph.nodes))
    try:
        route = nx.shortest_path(graph, start, end, weight="length")
        break
    except nx.NetworkXNoPath:
        continue

print("Route generated with", len(route), "nodes")
def get_lat_lon(node):
    return graph.nodes[node]["y"], graph.nodes[node]["x"]
ambulance_path = []

for node in route:
    lat, lon = get_lat_lon(node)
    ambulance_path.append((lat, lon))

    print(f"Ambulance at lat={lat:.6f}, lon={lon:.6f}")
    time.sleep(1)  # 1 second delay (GPS update rate)
fig, ax = ox.plot_graph(
    graph,
    node_size=0,
    edge_color="gray",
    show=False,
    close=False
)

for lat, lon in ambulance_path:
    ax.scatter(lon, lat, c="red", s=50)
    plt.pause(0.8)

plt.show()
