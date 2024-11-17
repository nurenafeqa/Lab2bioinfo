import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Replace with actual retrieval functions for PPI data
def retrieve_ppi_from_biogrid(protein_id):
    # Example: Return a dummy PPI dataframe (this would normally come from BioGRID API)
    return pd.DataFrame({
        "ProteinA": ["BRCA1", "BRCA1", "BRCA1"],
        "ProteinB": ["TP53", "EGFR", "MYC"]
    })

def retrieve_ppi_from_string(protein_id):
    # Example: Return a dummy PPI dataframe (this would normally come from STRING API)
    return pd.DataFrame({
        "ProteinA": ["BRCA1", "BRCA1", "BRCA1"],
        "ProteinB": ["MDM2", "AKT1", "ATM"]
    })

def build_network(ppi_data):
    # Build and return a NetworkX graph from the PPI data
    return nx.from_pandas_edgelist(ppi_data, source='ProteinA', target='ProteinB')

def calculate_centralities(graph):
    # Calculate multiple centrality measures for the network
    centrality_measures = {
        "Degree Centrality": nx.degree_centrality(graph),
        "Betweenness Centrality": nx.betweenness_centrality(graph),
        "Closeness Centrality": nx.closeness_centrality(graph),
        "Eigenvector Centrality": nx.eigenvector_centrality(graph),
        "PageRank": nx.pagerank(graph)
    }
    return centrality_measures

# Streamlit app layout
st.title("Protein-Protein Interaction Network")
st.write("This app visualizes Protein-Protein Interaction (PPI) data and computes centrality measures.")

# Input section (upper part)
st.header("Enter Protein Data")

# Protein ID text input (empty box, no default text)
protein_id = st.text_input("Enter Protein ID:")

# Dropdown for selecting PPI database
database_option = st.selectbox("Select Database:", ["BioGRID", "STRING"])

# Button to fetch PPI data
if st.button("Fetch PPI Data"):
    if not protein_id:
        st.error("Please enter a protein ID.")
    else:
        # Retrieve PPI data based on the selected database
        if database_option == "BioGRID":
            ppi_data = retrieve_ppi_from_biogrid(protein_id)
        elif database_option == "STRING":
            ppi_data = retrieve_ppi_from_string(protein_id)
        else:
            ppi_data = None

        # Check if the data was fetched successfully
        if ppi_data is not None and not ppi_data.empty:
            # Generate network graph
            graph = build_network(ppi_data)

            # Display results below the input section

            st.header("PPI Data and Network Overview")

            # Display PPI Data
            st.subheader("PPI Data")
            st.dataframe(ppi_data)

            # Display network statistics
            st.write(f"**Number of Nodes**: {graph.number_of_nodes()}")
            st.write(f"**Number of Edges**: {graph.number_of_edges()}")

            # Network Visualization
            st.write("**Network Visualization**")
            fig, ax = plt.subplots(figsize=(8, 6))
            pos = nx.spring_layout(graph)
            nx.draw_networkx(graph, pos, ax=ax, node_size=50, font_size=8, with_labels=True)
            st.pyplot(fig)

            # Display Centrality Measures
            st.header("Centrality Measures")

            centralities = calculate_centralities(graph)
            centrality_df = pd.DataFrame(centralities).T

            st.subheader("Centrality Data")
            st.dataframe(centrality_df)

            # Interpretation of centralities
            st.write("### Interpretation of Centrality Measures:")
            st.write("""
                - **Degree Centrality**: Higher degree indicates that the node is directly connected to many other nodes.
                - **Betweenness Centrality**: Nodes with high betweenness centrality act as bridges between other nodes.
                - **Closeness Centrality**: Nodes with high closeness centrality are closer to all other nodes in terms of path length.
                - **Eigenvector Centrality**: Nodes that are connected to high-centrality nodes also have high eigenvector centrality.
                - **PageRank**: A measure of node importance based on connections to other important nodes.
            """)
        else:
            st.error("No data found for this protein ID. Try a different ID or database.")
