from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from bokeh.plotting import figure

compras = pd.read_csv('compras.csv')
ventas = pd.read_csv('ventas.csv')
salidas = pd.read_csv('salidas.csv')
ventascompras = pd.read_csv('ventascompras.csv')

ventascompras['fecha'] = pd.to_datetime(ventascompras['fecha'], format='%d/%m/%Y')

ventascompras['mes'] = ventascompras['fecha'].dt.month
ventascompras['año'] = ventascompras['fecha'].dt.year

################## Sidebar ##################

st.sidebar.image('logo.png')

st.sidebar.title('Filtros')
st.sidebar.subheader('Filtrar por tiempo')

subset_data4 = ventascompras
unidad_input = st.sidebar.multiselect('Mes',
                                         ventascompras.groupby('mes').count().reset_index()['mes'].tolist())
if len(unidad_input) > 0:
    subset_data4 = ventascompras[ventascompras['mes'].isin(unidad_input)]

st.sidebar.subheader('Año')

subset_data3 = subset_data4
producto_input = st.sidebar.multiselect('Año',
                                         subset_data4.groupby('año').count().reset_index()['año'].tolist())
if len(producto_input) > 0:
    subset_data3 = subset_data4[subset_data4['año'].isin(producto_input)]