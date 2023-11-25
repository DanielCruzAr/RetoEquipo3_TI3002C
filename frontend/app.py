from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from bokeh.plotting import figure

def main():
    st.title('Police incident reports from 2018 to 2020 in San Francisco')

    df = pd.read_csv('Police_comp.csv')

    st.markdown('The data shown below belongs to incident reports in the City of San Francisco, from the year 2018 to 2020, woth details from each case such as date, day of the week, police district, neighbourhood in which it happened, type of incident in category and subcategory, exact location and resolution')

    mapa = pd.DataFrame()
    mapa['Date'] = df['Incident Date']
    mapa['Day'] = df['Incident Day of Week']
    mapa['District'] = df['Police District']
    mapa['Neighbourhood'] = df['Analysis Neighborhood']
    mapa['Incident Category'] = df['Incident Category']
    mapa['Incident Subcategory'] = df['Incident Subcategory']
    mapa['Resolution'] = df['Resolution']
    mapa['lat'] = df['Latitude']
    mapa['lon'] = df['Longitude']
    mapa = mapa.dropna()

    st.sidebar.title('Filter Options')

    subset_data4 = mapa
    police_district_input = st.sidebar.multiselect('Police District',
                                            mapa.groupby('District').count().reset_index()['District'].tolist())
    if len(police_district_input) > 0:
        subset_data4 = mapa[mapa['District'].isin(police_district_input)]

    subset_data3 = subset_data4
    neighbourhood_input = st.sidebar.multiselect('Neighbourhood',
                                            subset_data4.groupby('Neighbourhood').count().reset_index()['Neighbourhood'].tolist())
    if len(neighbourhood_input) > 0:
        subset_data3 = subset_data4[subset_data4['Neighbourhood'].isin(neighbourhood_input)]

    subset_data2 = subset_data3
    incident_input = st.sidebar.multiselect('Incident Category',
                                            subset_data3.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
    if len(incident_input) > 0:
        subset_data2 = subset_data3[subset_data3['Incident Category'].isin(incident_input)]

    subset_data1 = subset_data2
    incident_sub_input = st.sidebar.multiselect('Incident Subcategory',
                                            subset_data2.groupby('Incident Subcategory').count().reset_index()['Incident Subcategory'].tolist())
    if len(incident_sub_input) > 0:
        subset_data1 = subset_data2[subset_data2['Incident Subcategory'].isin(incident_sub_input)]

    subset_data = subset_data1
    resolution_input = st.sidebar.multiselect('Resolution',
                                            subset_data1.groupby('Resolution').count().reset_index()['Resolution'].tolist())
    if len(resolution_input) > 0:
        subset_data = subset_data1[subset_data1['Resolution'].isin(resolution_input)]    

    subset_data

    st.markdown('It is important to mention that any police district can answer to any incident, the neighbourhood in which it happened is not related to the police district')
    st.markdown('Crime locations in San Francisco')
    st.map(subset_data, color=(.1,.3,.6,.5))
    st.markdown('Crimes ocurred per day of the week')
    st.bar_chart(subset_data['Day'].value_counts())
    st.markdown('Crimes ocurred per date')
    st.bar_chart(subset_data['Date'].value_counts())
    st.markdown('Types of crimes committed')
    st.bar_chart(subset_data['Incident Category'].value_counts(),
                color = (.7,.3,.6,.5))

    agree = st.button('Click to see incident subcategories')
    if agree:
        st.markdown('Subtype of crimes committed')
        st.bar_chart(subset_data['Incident Subcategory'].value_counts())

    st.markdown('Resolution status')

    labels = subset_data['Resolution'].unique()
    values = subset_data['Resolution'].value_counts()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])

    st.plotly_chart(fig)

    st.markdown('Districts with the most crimes')

    labels2 = subset_data['District'].unique()
    values2 = subset_data['District'].value_counts()

    fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2, hole=.5)])

    st.plotly_chart(fig2)

    agree1 = st.button('Click to see neighbourhoods with the most crimes')
    if agree1:
        st.markdown('Neighbourhoods with the most crimes')
        labels3 = subset_data['Neighbourhood'].unique()
        values3 = subset_data['Neighbourhood'].value_counts()

        fig3 = go.Figure(data=[go.Pie(labels=labels3, values=values3, hole=.5)])

        st.plotly_chart(fig3)

if __name__ == '__main__':
    main()