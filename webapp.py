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

dev_column_names = {'v1.0': ['datetime', 'bateria', 'cmca']}
    

st.header("DataViz - Visualizador de datos")

tabs = st.tabs(["Principal", "Acerca de"])

principal = tabs[0]
acerca_de = tabs[1]
with principal:
    c1, c2, c3 = st.columns([2.5,0.6,0.5])

    uploaded_files = c1.file_uploader("Cargar archivos CSV", type=["csv"], accept_multiple_files=True)
    # version del dispositivo
    dev_version = c2.selectbox('Modelo dispositivo',('v1.0', 'v0.99'))
    if dev_version = "v1.0":
        column_names = dev_column_names[dev_version]
        column_datetime = column_names[0]
        c3.table(pd.DataFrame(column_names,columns=["Columna"]))
        if uploaded_files:
            dfs = (pd.read_csv(f, sep=";", parse_dates=[column_datetime], names=column_names, comment='#') for f in uploaded_files)
            eq = pd.concat(dfs, ignore_index=True)
            column_plot = st.columns(2)
            for i,column in enumerate(column_names[1:]):
                fig = go.Figure()
                fig.add_trace(go.Scattergl(x=eq[column_datetime], y=eq[column], name=column))
                fig.update_layout(title=column.upper(),xaxis_title=column_datetime)
                column_plot[(i+1)%2].plotly_chart(fig, use_container_width=True)
    else:
        st.write("versión no disponible")    
        #c4.dataframe(eq)    


    

with acerca_de:
    st.write("Programa:", "PySalado")
    st.write("Versión:",1.0)
    st.write("Dependencias:", "Python 3.8.5, Pandas, Numpy, Plotly")
    st.write("Fecha:", "08/11/2022")
    st.write("Autor:", "Mg. Ing. Emiliano P. López")
    st.write("Email:", "emiliano.lopez@gmail.com")