import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from generate_data import generate_dataset
from main import run_simulation
import shutil

st.set_page_config(page_title="Ambulance Routing Simulation", layout="wide")

st.title("🚑 Ambulance Routing with Dynamic Traffic")

# Sidebar - Configuration
st.sidebar.header("Simulation Parameters")

num_nodes = st.sidebar.slider("Number of Nodes", 50, 500, 100)
num_hospitals = st.sidebar.slider("Number of Hospitals", 1, 10, 5)
num_seconds = st.sidebar.slider("Simulation Duration (seconds)", 100, 2000, 500)
prob_edge = st.sidebar.slider("Edge Probability", 0.01, 0.2, 0.05)

data_dir = './csv_files'

# Main Content
tab1, tab2 = st.tabs(["Data Generation", "Run Simulation"])

with tab1:
    st.header("1. Generate Traffic & Network Data")
    st.write("Configure the parameters in the sidebar and click below to generate a new dataset.")
    
    if st.button("Generate New Dataset"):
        with st.spinner("Generating data..."):
            try:
                # Clean up old data if needed or just overwrite
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                
                success = generate_dataset(
                    num_nodes=num_nodes,
                    num_hospitals=num_hospitals,
                    num_seconds=num_seconds,
                    prob_edge=prob_edge,
                    output_dir=data_dir
                )
                
                if success:
                    st.success(f"Data successfully generated in `{data_dir}`!")
                    
                    # specific filess check
                    files = os.listdir(data_dir)
                    st.write(f"Generated {len(files)} files: {', '.join(files)}")
                    
                    # Preview Nodes
                    nodes_df = pd.read_csv(f"{data_dir}/nodes.csv", header=None, names=["X", "Y"])
                    hospitals_df = pd.read_csv(f"{data_dir}/hospital.csv", header=None, names=["X", "Y"])
                    
                    st.subheader("Network Preview")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.scatter(nodes_df['X'], nodes_df['Y'], c='blue', alpha=0.6, label='Nodes (Accident Prone)')
                    ax.scatter(hospitals_df['X'], hospitals_df['Y'], c='red', s=100, marker='P', label='Hospitals')
                    ax.legend()
                    ax.set_title("Network Topology")
                    st.pyplot(fig)
                    
            except Exception as e:
                st.error(f"Error generating data: {e}")

with tab2:
    st.header("2. Run Simulation")
    st.write("Run the ambulance routing simulation on the generated data.")
    
    if st.button("Start Simulation"):
        if not os.path.exists(f"{data_dir}/nodes.csv"):
            st.error("Data not found! Please generate data in the previous tab first.")
        else:
            with st.spinner("Running simulation..."):
                try:
                    results = run_simulation(data_dir)
                    
                    st.success("Simulation completed!")
                    
                    st.metric("Total Patients Transferred", results['patients_transferred'])
                    st.metric("Total Simulation Time", results['total_time'])
                    
                    # Visualization of results?
                    st.subheader("Simulation Stats")
                    st.write(f"Processed {len(results['simulation_data'])} rescue missions.")
                    
                    # Show a sample path
                    if results['simulation_data']:
                        st.subheader("Sample Ambualnce Path")
                        sample_mission = results['simulation_data'][0]
                        # [t, path, active_collisions]
                        path = sample_mission[1]
                        st.write(f"Path taken for a mission at time {sample_mission[0]}: {path}")
                        
                except Exception as e:
                    st.error(f"Simulation failed: {e}")
