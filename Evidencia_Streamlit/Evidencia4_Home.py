from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from backend.ml_model import predict_next_month, parse_data

# Fuente verdana
# st.set_page_config(font="verdana")

compras = pd.read_csv('compras.csv')
ventas = pd.read_csv('ventas.csv')
salidas = pd.read_csv('salidas.csv')
ventascompras = pd.read_csv('ventascompras.csv')

################## Sidebar ##################

# st.markdown("""
# <style>
#     [data-testid=stSidebar] {
#         background-color: #FAEAE3;
#     }
# </style>
# """, unsafe_allow_html=True)

st.sidebar.image('logo.png')

st.sidebar.title('Filtros')
st.sidebar.subheader('Existencias por unidad de medida')

subset_data4 = salidas
unidad_input = st.sidebar.multiselect('Unidad de medida',
                                         salidas.groupby('unidad').count().reset_index()['unidad'].tolist())
if len(unidad_input) > 0:
    subset_data4 = salidas[salidas['unidad'].isin(unidad_input)]

st.sidebar.subheader('Existencias por producto')

subset_data3 = subset_data4
producto_input = st.sidebar.selectbox('Producto',
                                         subset_data4.groupby('codigo_proveedor').count().reset_index()['codigo_proveedor'].tolist())
# if len(producto_input) > 0:
subset_data3 = subset_data4[subset_data4['codigo_proveedor'] == producto_input]

st.sidebar.subheader('Proyectar')

stock_unit = subset_data3["unidad"].unique()[0]
on = st.sidebar.toggle('Switch de proyección', value=False)
if not on:
    st.sidebar.write('Proyección desactivada')
else:
    if subset_data3.shape[0] < 300:
        st.sidebar.write('No hay suficientes datos para proyectar')
        on = False
    elif subset_data3["codigo_proveedor"].nunique() > 1:
        st.sidebar.write('Seleccione un único producto para proyectar')
        on = False
    else:
        subset_data3 = predict_next_month(subset_data3)



################## Primera página ##################

st.title('Existencias')
st.markdown('Cantidad de material en almacén')

################## Gráfica de productos con menos existencias ##################

# Filter the dataframe by the most recent dates
salidas1 = salidas.set_index("fecha")
most_recent_date = salidas1.index.max()
# Filter the dataframe for the most recent date
df_recent = salidas1[salidas1.index == most_recent_date]
# Group by codigo_proveedor and calculate the mean of "existencias"
df_recent = df_recent.groupby("codigo_proveedor")["existencias"].mean()
# Sort the dataframe by "existencias" in ascending order
df_sorted = df_recent.sort_values(ascending=False)

data = df_sorted.head(10)
fig = go.Figure(data=[go.Bar(
    x=data,
    y=data.index,
    orientation='h',
    marker=dict(color=data, coloraxis="coloraxis")
)])

fig.update_layout(width=800, height=400)
fig.update_xaxes(title_text="Existencias")
fig.update_yaxes(title_text="Productos")
fig.update_layout(title_text="Productos con menos existencias")
fig.update_layout(coloraxis=dict(colorscale="Reds_r"))
fig.update_layout(font_family="Verdana")

st.plotly_chart(fig)

################## Existencias por producto ##################
if not on:
    df_product = parse_data(subset_data3)
    columns = ["existencias"]
else:
    df_product = subset_data3
    columns = ["existencias", "limite superior", "limite inferior"]

fig1 = px.line(df_product, x=df_product.index, y=columns, color_discrete_sequence=px.colors.sequential.Reds_r)
fig1.update_layout(width=800, height=400)
fig1.update_xaxes(title_text="Fecha")
fig1.update_yaxes(title_text=f"Existencias ({stock_unit})")
fig1.update_layout(title_text="Existencias por Codigo de Proveedor")
fig1.update_layout(font_family="Verdana")
fig1.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1 día", step="day", stepmode="backward"),
                dict(count=7, label="1 sem", step="day", stepmode="backward"),
                dict(count=1, label="1 mes", step="month", stepmode="backward"),
                dict(count=6, label="6 mes", step="month", stepmode="backward"),
                dict(label="todos", step="all")
            ]
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

st.plotly_chart(fig1)