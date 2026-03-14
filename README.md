📌 Overview

Emergency response time is a critical factor in saving lives, especially in urban environments where traffic congestion significantly delays ambulances. This project presents a Smart Ambulance Rerouting & Green Corridor Traffic Control System that dynamically prioritizes ambulances by creating a real-time green corridor across traffic signals. The system ensures uninterrupted ambulance movement from the incident location to the hospital using intelligent routing and traffic signal control.

🎯 Problem Statement

In most cities, ambulances face severe delays due to traffic congestion and non-prioritized traffic signals. Existing traffic systems operate on fixed signal cycles and lack real-time coordination with emergency vehicles. This results in increased response time, higher risk to patients, and inefficient emergency management. There is a strong need for a smart, automated system that can dynamically reroute ambulances and control traffic signals in real time.

💡 Proposed Solution

This project proposes a software-based smart city solution where an ambulance is continuously tracked, and the most optimal route to the hospital is computed using real road network data. Traffic signals along this route are automatically overridden to GREEN, while conflicting directions are stopped, forming a moving green corridor. The system updates dynamically as the ambulance progresses, ensuring minimal delays and maximum efficiency.

🧠 System Architecture

The system follows a modular architecture consisting of a backend simulation engine, a traffic signal control module, and a web-based frontend dashboard. The backend uses real OpenStreetMap road data modeled as a graph, computes optimal routes, and simulates ambulance movement. A FastAPI server exposes real-time data, which is consumed by the frontend to visualize ambulance location and green traffic signals on a live map.

🛠️ Technologies Used

The backend is implemented using Python, FastAPI, OSMnx, and NetworkX for graph-based routing and simulation. OpenStreetMap data is used to model realistic urban road networks. The frontend is built using HTML, CSS, JavaScript, and Leaflet.js, providing a real-time, interactive map-based dashboard. The entire system is implemented as a 100% software simulation, without requiring any physical hardware.

🔄 Working Methodology

The system begins by loading a real city road network and selecting an ambulance start point and a hospital destination. The shortest path is computed using graph algorithms. The ambulance is then simulated to move node-by-node along this route. As the ambulance advances, traffic signals ahead of it are dynamically set to GREEN, while all others remain RED. This process repeats continuously, and updated location and signal data are sent to the frontend every second.

🖥️ Frontend Visualization

The frontend dashboard displays a real-time map with a moving ambulance icon and green signal markers indicating the active green corridor. A control panel shows live ambulance coordinates and system status, making the interface intuitive and operator-friendly. This visualization demonstrates how backend intelligence is transformed into actionable, human-readable insights suitable for smart city control centers.

✅ Features

The system supports real-time ambulance tracking, optimal route computation, dynamic traffic signal preemption, and live visualization. It uses real-world map data and follows a clean separation between backend logic and frontend presentation. The architecture is scalable and can be extended to support multiple ambulances, real traffic data, or machine learning–based congestion prediction.

🚀 Applications

This system can be applied in smart cities, emergency medical services, police and fire vehicle prioritization, and urban traffic management systems. With real-world integration, it can significantly reduce emergency response times and improve public safety outcomes.

🔮 Future Enhancements

Future work includes integrating real-time traffic density data, implementing machine learning models for congestion prediction, supporting multiple emergency vehicles with priority handling, adding ETA comparison metrics, and deploying the system on cloud infrastructure. Hardware integration with real traffic lights and GPS-enabled ambulances can further enhance real-world applicability.

🏁 Conclusion

The Smart Ambulance Rerouting & Green Corridor Traffic Control System demonstrates how intelligent routing, real-time data processing, and smart traffic control can transform emergency response systems. By combining graph algorithms, API-driven architecture, and live geospatial visualization, this project provides a practical and scalable solution for modern smart cities.
