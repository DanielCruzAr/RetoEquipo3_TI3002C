from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from bokeh.plotting import figure

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
producto_input = st.sidebar.multiselect('Producto',
                                         subset_data4.groupby('codigo_proveedor').count().reset_index()['codigo_proveedor'].tolist())
if len(producto_input) > 0:
    subset_data3 = subset_data4[subset_data4['codigo_proveedor'].isin(producto_input)]

st.sidebar.subheader('Proyectar')

on = st.sidebar.toggle('Switch de proyección', value=False)
if not on:
    st.sidebar.write('Proyección desactivada')
else:
    st.sidebar.write('Proyección activada')


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

metros = salidas[salidas["unidad"] == "M"]
top_categories = metros["codigo_proveedor"].value_counts().head(1).index
top_prod = metros[metros["codigo_proveedor"].isin(top_categories)]

fig1 = px.line(top_prod, x=top_prod.index, y="existencias", color_discrete_sequence=px.colors.sequential.Reds_r)
fig1.update_layout(width=800, height=400)
fig1.update_xaxes(title_text="Fecha")
fig1.update_yaxes(title_text="Existencias (M)")
fig1.update_layout(title_text="Existencias por Codigo de Proveedor")
fig1.update_layout(font_family="Verdana")

st.plotly_chart(fig1)

'''
################## Gráfica compras y ventas ##################

ventascompras['fecha'] = pd.to_datetime(ventascompras['fecha'], dayfirst=True)
ventascompras['año'] = ventascompras['fecha'].dt.year

df1 = ventascompras.sort_values(by=['fecha'], ascending=[True])
fig1 = px.line(df1, x='fecha', y='total_monto', color='movimiento',
              title='Compras y ventas de productos con mayor importancia',
              labels={'fecha': 'Fecha', 'total_monto': 'Monto en Pesos'},
              hover_name='producto',
              hover_data=['cantidad', 'total_monto'],
              color_discrete_map={'venta': 'green', 'compra': '#90131C'},
              markers=True,
              )

fig1.update_layout(
    font_family='Verdana',
    font_color='Black',
    font_size=14,
    title={
        'text': 'Compras y ventas de productos con mayor importancia',
        'x': 0.5,
        'y': 0.9
    },
    legend={'x': 1, 'y': 0.5},
    # plot_bgcolor='White',
    xaxis=dict(gridcolor='#D9D9D9'),
    yaxis=dict(gridcolor='#D9D9D9')
)

st.plotly_chart(fig1)
'''