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
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
mes_input = st.sidebar.multiselect('Mes', meses)
mes_numerico = [meses.index(mes) + 1 for mes in mes_input]
if len(mes_numerico) > 0:
    subset_data4 = ventascompras[ventascompras['mes'].isin(mes_numerico)]

subset_data3 = subset_data4
year_input = st.sidebar.multiselect('Año',
                                         subset_data4.groupby('año').count().reset_index()['año'].tolist())
if len(year_input) > 0:
    subset_data3 = subset_data4[subset_data4['año'].isin(year_input)]

st.sidebar.subheader('Filtrar por producto')

subset_data2 = subset_data3
producto_input = st.sidebar.multiselect('Producto',
                                         subset_data3.groupby('producto').count().reset_index()['producto'].tolist())
if len(producto_input) > 0:
    subset_data2 = subset_data3[subset_data3['producto'].isin(producto_input)]

################## Finanzas ##################

st.title('Finanzas')
st.markdown('Estado general de las finanzas de Calor y Control')

################## Primera parte ##################

################## Pie de top 10 prods ##################

df_sorted = subset_data4[subset_data4['movimiento'] == 'venta']
df_sorted = df_sorted.nlargest(10, 'cantidad')
fig = go.Figure(data=[go.Pie(
    labels=df_sorted['producto'],
    values=df_sorted['cantidad'],
    hole=0.5,
    marker=dict(colors=px.colors.sequential.Reds_r),
    textinfo='value',
    textposition='inside',
)])

if len(mes_input) > 0:
    fig.update_layout(
        font_family='Verdana',
        # font_color='#90131C',
        title={
            'text': f'Top 10 productos más vendidos en {mes_input}',
            # 'x': 0.5,
            # 'y': 0.9
        },
        font_size=14,
        legend={'x': 1, 'y': 0.5}
    )

else:
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

st.plotly_chart(fig)

################## Segunda parte ##################

################## Gráfica cantidad  vs. importe ##################

productos = subset_data2['producto'].tolist()

fig2 = px.scatter(subset_data2, x='cantidad', y='total_monto', color='producto',
                 title='Gráfica Cantidad vs Importe', color_continuous_scale='Reds_r',
                 hover_data=['producto', 'cantidad', 'total_monto', 'movimiento'],)

fig2.update_layout(
    xaxis_title='Cantidad',
    yaxis_title='Importe',
    title={
        'text': 'Gráfica Cantidad vs Importe',
        # 'x': 0.5,
        # 'y': 0.9,
        # 'xanchor': 'center',
        # 'yanchor': 'top'
    },
    legend_title='Producto'
)

st.plotly_chart(fig2)

################## Tercera parte ##################

################## Gráfica compras y ventas ##################

df1 = subset_data2.sort_values(by=['fecha'], ascending=[True])
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
        # 'x': 0.5,
        # 'y': 0.9,
        # 'xanchor': 'center',
        # 'yanchor': 'top'
    },
    legend={'x': 1, 'y': 0.5},
    # plot_bgcolor='White',
    xaxis=dict(gridcolor='#D9D9D9'),
    yaxis=dict(gridcolor='#D9D9D9')
)

st.plotly_chart(fig3)