import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime

from numpy.polynomial import polynomial

from pathlib import Path

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

dev_column_names = {'v2.0': ['datetime', 'bateria', 'cmca'],
                    'v4.0': ['datetime', 'bateria', 'nf', 'cmca'],
                    }
    

st.header("DataViz - Visualizador de datos")

tabs = st.tabs(["Principal", "Datos Calibración", "Acerca de"])

principal = tabs[0]
calibracion = tabs[1]
acerca_de = tabs[2]
with principal:
    c1, c2, c3 = st.columns([2.5,0.6,0.5])

    uploaded_files = c1.file_uploader("Cargar archivos CSV", type=["csv"], accept_multiple_files=True)
    # version del dispositivo
    dev_version = c2.selectbox('Modelo dispositivo',('v2.0', 'v4.0'))
    if dev_version in dev_column_names:
        column_names = dev_column_names[dev_version]
        column_datetime = column_names[0]
        c3.table(pd.DataFrame(column_names, columns=["Columnas"]))
        if uploaded_files:
            dfs = (pd.read_csv(f, sep=";", parse_dates=[column_datetime], names=column_names, comment='#') for f in uploaded_files)
            eq = pd.concat(dfs, ignore_index=True)
            eq.sort_values(by=column_datetime, inplace = True) 
            column_plot = st.columns(2)
            for i,column in enumerate(column_names[1:]):
                fig = go.Figure()    
                fig.add_trace(go.Scattergl(x=eq[column_datetime], y=eq[column], name=column, mode="lines+markers"))
                fig.update_layout(title=column.upper(), xaxis_title=column_datetime)
                if column == "nf":
                    fig.update_yaxes(autorange="reversed")
                column_plot[(i+1)%2].plotly_chart(fig, use_container_width=True)
    else:
        st.write("versión no disponible")    
        #c4.dataframe(eq)    


with calibracion:
    serial_number = st.text_input('Número serie del dispositivo (SN)', "")
    if serial_number == "0021":
        cwd = Path.cwd()
        fn  = cwd / "calib_data" / "dev_sn_0021.csv"
        data = pd.read_csv(fn, sep=";")
        xdata = data["sensor"]
        ydata = data["manual"]

        # ajuste lineal
        c, stats = polynomial.polyfit(xdata,ydata,1,full=True)
        x = np.arange(0,870,0.1)
        y = x*c[1] + c[0]
        # calculo R2
        corr_matrix = np.corrcoef(ydata, xdata)
        corr = corr_matrix[0,1]
        R2 = corr**2
        # curva de ajuste lineal
        st.write("**Curva de ajuste:**")
        st.latex(f"y={str(c[1])[0:7]}x + {str(c[0])[0:7]},\quad R^2={str(R2)[0:7]}")
        # figura con scatter, curva de ajuste y curva ideal 1:1
        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=xdata, y=ydata, mode="markers", name="Datos"))
        fig.add_trace(go.Scattergl(x=x, y=y, mode="lines", name=f"Ajuste"))
        fig.add_trace(go.Scattergl(x=[0,780], y=[0,780], mode='lines', name="1:1", line = dict(color='gray', width=2, dash='dash')))

        fig.update_layout(title=f"Datos de calibración", xaxis_title="Columna Agua Sensor [cm]", yaxis_title="Columna Agua Manual [cm]")
        fig.update_layout(autosize=False, width = 700, height = 700)
        fig.update_layout(font  = dict(family = "Calibri", size = 20,),)

        fig.update_layout(
            xaxis = dict(
                showline = True,
                linecolor = 'black',
                showgrid = True, 
                tickfont = dict(
                        family = 'Calibri'
                    )),
            yaxis = dict(
                showline = True,
                showgrid = True,
                linecolor = 'black', 
                tickfont = dict(
                    family = 'Calibri'
                )
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            template = 'plotly_white', 

        )
        st.plotly_chart(fig, use_container_width=False)
    else:
        st.write("Equipo no encontrado!")


with acerca_de:
    st.write("Programa:", "PyDataViz")
    st.write("Versión:",1.0)
    st.write("Fecha:", "21/03/2023")
    st.write("Autor:", "Mg. Ing. Emiliano P. López")
    st.write("Email:", "emiliano.lopez@gmail.com")
