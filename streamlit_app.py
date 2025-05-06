import streamlit as st
import time
import networkx as nx
import matplotlib.pyplot as plt

# Setup Streamlit page
st.set_page_config(page_title="BFS Visualization with Queue", layout="centered")
st.title("🔁 BFS Traversal with Queue Visualization")

# Default graph (directed)
default_graph = {
    "Austin": ["Dallas", "Houston"],
    "Dallas": ["Denver", "Austin", "Chicago"],
    "Houston": ["Atlanta"],
    "Chicago": ["Denver"],
    "Denver": ["Chicago", "Atlanta"],
    "Atlanta": ["Washington", "Houston"],
    "Washington": ["Atlanta", "Dallas"]
}

# Sidebar for graph customization
st.sidebar.header("Graph Setup")
custom_graph = st.sidebar.checkbox("Use custom graph?")
if custom_graph:
    graph_input = st.sidebar.text_area(
        "Graph as adjacency list (e.g., A:B,C)",
        value="A:B,C\nB:D,E\nC:F\nD:\nE:F\nF:"
    )
    graph = {}
    for line in graph_input.strip().splitlines():
        if ':' in line:
            node, neighbors = line.split(':')
            graph[node.strip()] = [n.strip() for n in neighbors.split(',') if n.strip()]
else:
    graph = default_graph

start_node = st.sidebar.selectbox("Start Node", list(graph.keys()))

# BFS with Queue Visualization and Bidirectional Arrows
def bfs_with_queue(graph, start):
    visited = set()
    queue = [start]
    traversal = []

    # Create MultiDiGraph to allow bidirectional arrows
    G = nx.MultiDiGraph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)

    # Initial graph view
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, ax=ax)
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        connectionstyle='arc3,rad=0.2',
        arrows=True,
        edge_color='gray'
    )
    st.pyplot(fig)

    while queue:
        current = queue.pop(0)
        traversal.append(current)
        visited.add(current)

        # Determine node colors
        node_colors = []
        for node in G.nodes():
            if node == current:
                node_colors.append('red')
            elif node in visited:
                node_colors.append('green')
            elif node in queue:
                node_colors.append('orange')
            else:
                node_colors.append('lightblue')

        # Draw graph with updated colors
        fig, ax = plt.subplots()
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors)
        nx.draw_networkx_labels(G, pos, ax=ax)
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            connectionstyle='arc3,rad=0.2',
            arrows=True,
            edge_color='gray'
        )
        st.pyplot(fig)

        # Display status
        st.write(f"🔵 **Current Node**: `{current}`")
        st.write(f"📥 **Queue**: `{queue}`")
        st.write(f"✅ **Visited**: `{list(visited)}`")

        # Enqueue unvisited neighbors
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)

        time.sleep(1)

    return traversal

# Run visualization
if st.button("Start BFS Visualization"):
    st.subheader(f"🔍 BFS from `{start_node}`")
    bfs_order = bfs_with_queue(graph, start_node)
    st.success(f"✅ Traversal Order: {' → '.join(bfs_order)}")
