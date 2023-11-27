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

################## Finanzas ##################

st.title('Finanzas')
st.markdown('Estado general de las finanzas de Calor y Control')

################## Primera parte ##################

c1, c2 = st.columns(2)

df_sorted = ventas.nlargest(10, 'ventas_cant')
fig = go.Figure(data=[go.Pie(
    labels=df_sorted['producto'],
    values=df_sorted['ventas_cant'],
    hoverinfo='label+percent',
    hole=0.5,
    marker=dict(colors=px.colors.sequential.Reds_r),
    # title='Top 10 productos más vendidos',
    textinfo='value',
    textposition='inside',
)])

fig.update_layout(
    font_family='Verdana',
    # font_color='#90131C',
    title={
        'text': 'Top 10 productos más vendidos',
        # 'x': 0.5,
        # 'y': 0.9
    },
    font_size=14,
    legend={'x': 1, 'y': 0.5}
)

c1.plotly_chart(fig)

ventas['total_almacen'] = ventas['costo_prom'] * ventas['existencias']
total_almacen_sum = ventas['total_almacen'].sum()

formatted_sum = f"${total_almacen_sum/1000000:.2f} M"
c2.error(f"{formatted_sum} \nTotal de producto en almacén")

################## Segunda parte ##################

productos = ventascompras['producto'].tolist()

import plotly.express as px

fig2 = px.scatter(ventascompras, x='cantidad', y='total_monto', color='producto',
                 title='Gráfica Cantidad vs Importe', color_continuous_scale='Reds_r')

fig2.update_layout(
    xaxis_title='Cantidad',
    yaxis_title='Importe',
    legend_title='Producto'
)

st.plotly_chart(fig2)

################## Tercera parte ##################

################## Gráfica compras y ventas ##################

ventascompras['fecha'] = pd.to_datetime(ventascompras['fecha'], dayfirst=True)
ventascompras['año'] = ventascompras['fecha'].dt.year

df1 = ventascompras.sort_values(by=['fecha'], ascending=[True])
fig3 = px.line(df1, x='fecha', y='total_monto', color='movimiento',
              title='Compras y ventas de productos con mayor importancia',
              labels={'fecha': 'Fecha', 'total_monto': 'Monto en Pesos'},
              hover_name='producto',
              hover_data=['cantidad', 'total_monto'],
              color_discrete_map={'venta': 'green', 'compra': '#90131C'},
              markers=True,
              )

fig3.update_layout(
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

st.plotly_chart(fig3)