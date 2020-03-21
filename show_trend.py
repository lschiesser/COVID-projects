import pandas as pd
import plotly.graph_objects as go
import streamlit as st

archive = pd.read_csv('archive.csv')
fig = go.Figure()
for i in archive.columns[1:]:
    fig.add_trace(go.Scatter(
                x=archive.retrieval_time,
                y=archive[i],
                name=i))

st.plotly_chart(fig)
