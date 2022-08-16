import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    page_title='Social Network Demo',
    page_icon='🔗', layout="centered")
st.title('Social Network Demo')
st.markdown('Author: [Ruslan Klymentiev](https://rklymentiev.com/)')

# st.sidebar.subheader('Set-up:')
algorithm = st.sidebar.selectbox(
    label='Select the Network Type:',
    options=('Complete Graph', 'Erdos-Renyi Graph', 'Balanced Tree',
             'Binomial Tree', 'Newman–Watts–Strogatz small-world', 'Barabasi-Albert Graph',
             'Random Lobster Graph', 'Random Regular Graph'),
    index=0)

if algorithm == 'Complete Graph':
    n = st.sidebar.slider(
        label='n',
        help='Number of nodes',
        value=10, min_value=1, max_value=20, step=1)
    G = nx.complete_graph(n)

elif algorithm == 'Erdos-Renyi Graph':
    n = st.sidebar.slider(label='Number of Nodes:', value=10, min_value=1, max_value=20, step=1)
    p = st.sidebar.slider(label='Probability of Connection:', value=0.5, min_value=0.0, max_value=1.0, step=0.05)
    G = nx.erdos_renyi_graph(n, p)

elif algorithm == 'Balanced Tree':
    n = st.sidebar.slider(label='Branching factor of the tree:', value=5, min_value=1, max_value=8, step=1)
    k = st.sidebar.slider(label='Height of the tree:', value=2, min_value=1, max_value=4, step=1)
    G = nx.balanced_tree(n, k)

elif algorithm == 'Binomial Tree':
    n = st.sidebar.slider(label='Order of the tree:', value=2, min_value=1, max_value=8, step=1)
    G = nx.binomial_tree(n)

elif algorithm == 'Newman–Watts–Strogatz small-world':
    n = st.sidebar.slider(label='Number of Nodes:', value=10, min_value=1, max_value=20, step=1)
    k = st.sidebar.slider(label='Number of nearest neighbors:', value=1, min_value=1, max_value=n, step=1)
    p = st.sidebar.slider(label='Probability of rewiring:', value=0.1, min_value=0.0, max_value=1.0, step=0.05)
    G = nx.newman_watts_strogatz_graph(n, k, p)

elif algorithm == 'Barabasi-Albert Graph':
    n = st.sidebar.slider(label='Number of Nodes:', value=10, min_value=1, max_value=20, step=1)
    m = st.sidebar.slider(label='Number of edges to attach from a new node:', value=1, min_value=1, max_value=n-1, step=1)
    G = nx.barabasi_albert_graph(n, m)

elif algorithm == 'Random Lobster Graph':
    n = st.sidebar.slider(label='The expected number of nodes in the backbone:', value=10, min_value=1, max_value=20, step=1)
    p1 = st.sidebar.slider(label='Probability of adding an edge to the backbone:', value=0.1, min_value=0.0, max_value=1.0, step=0.05)
    p2 = st.sidebar.slider(label='Probability of adding an edge one level beyond backbone:', value=0.1, min_value=0.0,
                                 max_value=1.0, step=0.05)
    G = nx.random_lobster(n, p1, p2)

elif algorithm == 'Random Regular Graph':
    n = st.sidebar.slider(label='The number of nodes: The value of n x d must be even.', value=5, min_value=2, max_value=20, step=1)
    d = st.sidebar.slider(label='The degree of each node:', value=0, min_value=0, max_value=n-1, step=2)
    G = nx.random_regular_graph(d, n)

tab1, tab2 = st.tabs(["Graph Visualization", "Centrality Measurements"])

with tab1:
    # fig = nx.draw(G, with_labels=True, font_weight='bold')
    # st.pyplot(fig)

    nt = Network(font_color="black")
    nt.from_nx(G)
    for n in range(len(nt.nodes)):
        nt.nodes[n]['label'] = str(nt.nodes[n]['label'])
        # nt.nodes[n]['title'] = parser
    nt.show('test.html')
    HtmlFile = open("test.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()

    components.html(source_code, height = 900,width=900)

with tab2:
    df = pd.DataFrame({})
    df = pd.concat(
        [df, pd.DataFrame(nx.degree_centrality(G), index=['Degree']).T,
         pd.DataFrame(nx.eigenvector_centrality(G), index=['Eigenvector']).T,
         pd.DataFrame(nx.betweenness_centrality(G), index=['Betweenness']).T,
         ],
        axis=1)

    df.reset_index(inplace=True, drop=False)
    df.rename(columns={'index': 'Node'}, inplace=True)

    st.dataframe(df)
