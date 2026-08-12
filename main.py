import math
import numpy as np
import csv
import shortest_path as sp
from functions import *
import os

def run_simulation(data_dir='./csv_files'):
    # initialize all arrays
    trafficData = []
    collisionData = []
    adjM = []
    nodes = []
    edges = []
    nodes_dict = {}
    edges_dict = {}
    hospitals = []
    active_collisions = [] # contains nodes for all active collision
    current_ambulance_locations = []
    simulation_data = []

    # Read Data
    with open(f'{data_dir}/trafficData.csv', 'r') as csvfile:
        read = csv.reader(csvfile)
        for r in read:
            trafficData.append(list(map(float, r)))
    trafficData = np.asarray(trafficData)
    print('traffic data', trafficData.shape)

    with open(f'{data_dir}/collisionData.csv', 'r') as csvfile: 
        read = csv.reader(csvfile) 
        for r in read: 
            collisionData.append(list(map(float, r)))
    collisionData = np.asarray(collisionData)
    print('collision data', collisionData.shape)

    with open(f'{data_dir}/adjM_new.csv', 'r') as csvfile: 
        read = csv.reader(csvfile) 
        for r in read: 
            adjM.append(list(map(float, r)))
    adjM = np.asarray(adjM)
    adjM = adjM.astype(int)
    print('adjm', adjM.shape)

    with open(f'{data_dir}/hospital.csv', 'r') as csvfile: 
        read = csv.reader(csvfile) 
        for r in read: 
            hospitals.append(list(map(float, r)))
    hospitals = np.asarray(hospitals)

    with open(f'{data_dir}/nodes.csv', 'r') as csvfile: 
        read = csv.reader(csvfile) 
        count = 0
        for r in read:
            nodes_dict[count] = r
            count += 1
            nodes.append(list(map(float, r)))
    nodes = np.asarray(nodes)

    with open(f'{data_dir}/edges_new.csv', 'r') as csvfile: 
        read = csv.reader(csvfile) 
        count = 0
        for r in read:
            edges_dict[(int(float(r[0])), int(float(r[1])))] = count
            count += 1
            edges.append(list(map(float, r)))
    edges = np.asarray(edges)

    number_of_seconds, number_of_edges = trafficData.shape
    number_of_collision = collisionData.shape[0]
    number_of_nodes = nodes.shape[0]
    number_of_ambulances = hospitals.shape[0]
    number_of_hospitals = number_of_ambulances

    # this is for making adj matrix consistent with the edges file
    num_hospital_edges = edges.shape[0] - trafficData.shape[1]
    hospital_connections = np.ones((number_of_seconds, num_hospital_edges)) * 20
    updatedTrafficData = np.concatenate((trafficData, hospital_connections), axis=1)
    nodes_all = np.concatenate((nodes, hospitals), axis=0)

    # initialising the ambulance locations
    for i in range(number_of_hospitals):
        current_ambulance_locations.append([hospitals[i, 0], hospitals[i, 1]])

    amb_locs_history = [] # Track ambulance locations over time

    num_collisions_at_that_time = 0
    patients_transferred = 0

    # dict for storing the number of patients currently each hospital has
    # Assuming dynamic allocation or fixed? 
    # Original code had hardcoded dict causing issues if num_hospitals != 5
    hospital_ambulance_dict = {}
    for i in range(number_of_hospitals):
        hospital_ambulance_dict[number_of_nodes + i] = i

    # how much time has passed for each patient as we have release each 
    hospital_allocation_timings = {}
    for i in range(number_of_hospitals):
        hospital_allocation_timings[number_of_nodes + i] = []

    # dict for storing all patients (nodes where accidents took place) for each hospital
    ambulance_casualty_dict = {}
    for i in range(number_of_ambulances):
        ambulance_casualty_dict[i] = []
        
    ambulance_availability = [0]*number_of_ambulances
    hospital_vacancy = [0]*number_of_hospitals

    for t in range(number_of_seconds):
        while (num_collisions_at_that_time < number_of_collision and collisionData[num_collisions_at_that_time, 0] <= t): # changed == t to <= t to catch up
            active_collisions.append(collisionData[num_collisions_at_that_time, 1])
            num_collisions_at_that_time += 1
        
        # constructing the graph using all the edges and nodes provided
        g = sp.Graph(number_of_nodes + number_of_hospitals)

        for i1 in range(number_of_nodes + number_of_hospitals):
            for j1 in range(number_of_nodes + number_of_hospitals):
                if ((adjM[i1, j1] == 1) and (i1!=j1)):
                    speed = updatedTrafficData[t, edges_dict[(i1, j1)]-1]
                    distance = distance_between_nodes(i1, j1, nodes_all)
                    time_val = distance / speed
                    g.addEdge(i1, j1, time_val)
                    
        for some_num in ambulance_casualty_dict.keys():
            for some_num1 in ambulance_casualty_dict[some_num]:
                if(t >= some_num1[2]):
                    ambulance_casualty_dict[some_num].remove(some_num1)
        for some_num in hospital_allocation_timings.keys():
            for some_num1 in hospital_allocation_timings[some_num]:
                if(t >= some_num1):
                    hospital_vacancy[some_num - number_of_nodes] -= 1
                    hospital_allocation_timings[some_num].remove(some_num1)

        # we iterate over all active collisions in order to assign them corresponding ambulances
        trajectory_ambulance = []
        
        # Make a copy to iterate safely while modifying original list
        for ac in list(active_collisions):

            # node at which the accident has occurred at
            active_node = (int)(ac)

            # using shortest path from a source algorithm
            ac_distances, p = np.asarray(g.BellmanFord(active_node))

            hospital_distances_list = ac_distances[number_of_nodes:]
            nearest_hospital = number_of_nodes + np.argmin(ac_distances[number_of_nodes:]) 
            
            assigned_ambulance = hospital_ambulance_dict.get(nearest_hospital, 0)

            # this path is the set of all nodes that are traversed to reach casualty and then to hospital
            path = generate_path(p, np.argmin(ac_distances[number_of_nodes:]), active_node)

            # this temp variable depicts if the accident is currently alloted or not
            if (ambulance_availability[assigned_ambulance] == 0):
                temp = 1 
            else:
                temp = 0

            # initially filling infinity at all edges
            min_dist = float('inf') 
            min_dist_index = -1

            # if accident is unassigned
            if (temp == 0):
                start_check = 0 # Dummy logic to simulate while loop behavior if needed?
                # Actually, iterate through all hospitals to find nearest available
                # Original logic: while(ambulance_availability[assigned_ambulance] != 0): ...
                # It tries to find another hospital
                best_alternative = -1
                for hos in range(number_of_hospitals):
                    if(hospital_distances_list[hos] < min_dist and ambulance_availability[hos] == 0 and hospital_vacancy[hos] < 10):
                        min_dist = hospital_distances_list[hos]
                        min_dist_index = hos
                        best_alternative = hos
                
                if best_alternative != -1:
                    assigned_ambulance = best_alternative
                    temp = 1

            # if accident is assigned 
            if (temp == 1):
                ambulance_availability[assigned_ambulance] = 1
                hospital_vacancy[nearest_hospital - number_of_nodes] += 1 
                hospital_allocation_timings[nearest_hospital].append(t + 1800) 
               
                time_required_to_drop_patient = 2 * ac_distances[nearest_hospital] 
                
                ambulance_casualty_dict[assigned_ambulance].append([active_node, t, t+time_required_to_drop_patient])
                simulation_data.append([t, path, active_collisions])
                
                if ac in active_collisions:
                    active_collisions.remove(ac)
                patients_transferred += 1

            # this path is for simulation
            trajectory_ambulance.append([active_node, assigned_ambulance, path])
            
        amb_locs_history.append(list(current_ambulance_locations)) # Snapshot of locations (logic for movement missing in original)

        if(t == 50000):
            break
            
    return {
        'simulation_data': simulation_data,
        'nodes': nodes,
        'hospitals': hospitals,
        'patients_transferred': patients_transferred,
        'total_time': number_of_seconds
    }

if __name__ == "__main__":
    run_simulation()
