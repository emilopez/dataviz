import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime


#today_icon = random.choice(["🧉", "📉", "💧","🦩","🦟","🌎", "🇦🇷","🌅","🌉"]) #https://emojipedia.org/
st.set_page_config(
     page_title="DataViz | Visualizador de datos",
     page_icon="🇦🇷",
     layout="wide",
     initial_sidebar_state="collapsed",
)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

    

st.header("DataViz - Visualizador de datos")

tabs = st.tabs(["Principal", "Acerca de"])

principal = tabs[0]
acerca_de = tabs[1]
with principal:
    c1, c2, c3, c4 = st.columns([1.7,0.3,2.1,2.1])

    uploaded_files = c1.file_uploader("Cargar archivos CSV", type=["csv"], accept_multiple_files=True)
    desde_n_dias = c2.selectbox("Días previos", (7, 50, 100))
    if uploaded_files:
        dfs = (pd.read_csv(f, sep=";", parse_dates=['datetime'], names=['datetime', 'bateria', 'cmca'], comment='#') for f in uploaded_files)
        eqPuntano = pd.concat(dfs, ignore_index=True)
        st.write(eqPuntano)    

    

with acerca_de:
    st.write("Programa:", "PySalado")
    st.write("Versión:",1.0)
    st.write("Dependencias:", "Python 3.8.5, Pandas, Numpy, Plotly")
    st.write("Fecha:", "08/11/2022")
    st.write("Autor:", "Mg. Ing. Emiliano P. López")
    st.write("Email:", "emiliano.lopez@gmail.com")