import numpy as np
import csv
import os
import random

def generate_dataset(num_nodes=100, num_hospitals=5, num_seconds=500, prob_edge=0.05, output_dir='./csv_files'):
    # Configuration
    GRID_SIZE = 1000

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Generating data in {output_dir}...")

    # 1. Generate Nodes (0 to NUM_NODES-1)
    nodes = np.random.rand(num_nodes, 2) * GRID_SIZE
    with open(f'{output_dir}/nodes.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(nodes)
    print(f"Generated {num_nodes} nodes.")

    # 2. Generate Hospitals (NUM_NODES to NUM_NODES+NUM_HOSPITALS-1)
    hospitals = np.random.rand(num_hospitals, 2) * GRID_SIZE
    with open(f'{output_dir}/hospital.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(hospitals)
    print(f"Generated {num_hospitals} hospitals.")

    # 3. Generate Edges & Adj Matrix
    total_vertices = num_nodes + num_hospitals
    adjM = np.zeros((total_vertices, total_vertices), dtype=int)
    edges_node = []
    edges_hospital = []

    # Generate random edges between nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < prob_edge:
                adjM[i][j] = 1
                adjM[j][i] = 1
                edges_node.append([i, j, 1.0]) 
                edges_node.append([j, i, 1.0])

    # Generate edges connecting hospitals to nearest nodes
    for h_idx in range(num_hospitals):
        h_node_idx = num_nodes + h_idx
        # Connect to k nearest nodes
        dists = []
        for n_idx in range(num_nodes):
            d = np.linalg.norm(hospitals[h_idx] - nodes[n_idx])
            dists.append((d, n_idx))
        dists.sort()
        
        # Connect to 3 nearest nodes
        for k in range(3):
            n_idx = dists[k][1]
            adjM[h_node_idx][n_idx] = 1
            adjM[n_idx][h_node_idx] = 1
            edges_hospital.append([h_node_idx, n_idx, 1.0])
            edges_hospital.append([n_idx, h_node_idx, 1.0])

    # Save Adj Matrix
    np.savetxt(f'{output_dir}/adjM_new.csv', adjM, delimiter=",", fmt='%d')
    print("Generated adjacency matrix.")

    # Save Edges
    all_edges = edges_node + edges_hospital
    with open(f'{output_dir}/edges_new.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_edges)
    print(f"Generated {len(all_edges)} edges.")

    # 4. Generate Traffic Data
    num_node_edges = len(edges_node)
    
    # Generate random speeds (20 to 60)
    traffic_data = np.random.uniform(20, 60, (num_seconds, num_node_edges))
    with open(f'{output_dir}/trafficData.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(traffic_data)
    print(f"Generated traffic data for {num_seconds} seconds.")

    # 5. Generate Collision Data
    collisions = []
    for t in range(0, num_seconds, 50): # Every 50 seconds
        if random.random() < 0.8:
            node_idx = random.randint(0, num_nodes - 1)
            collisions.append([t, node_idx])

    with open(f'{output_dir}/collisionData.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(collisions)
    print(f"Generated {len(collisions)} collisions.")
    return True

if __name__ == "__main__":
    generate_dataset()
