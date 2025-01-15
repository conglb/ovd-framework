import streamlit as st
from influxdb_client import InfluxDBClient
import pandas as pd
import plotly.express as px
from datetime import datetime
import psycopg2

# TimscaleDB connection configuration
CONNECTION = "dbname=ovd user=admin password=admin host=localhost port=5432"
conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

# Function to query AIS data from InfluxDB
def query_ais_data(start_date, end_date):
    query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {start_date}, stop: {end_date})
        |> filter(fn: (r) => r._measurement == "test1")
        |> filter(fn: (r) => r._field == "Latitude" or r._field == "Longitude")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> keep(columns: ["_time", "Latitude", "Longitude"])
    '''
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        query_api = client.query_api()
        result = query_api.query_data_frame(query)
        return result

# Streamlit app layout
st.title("AIS Data Viewer")

# Sidebar for date range selection
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", datetime(2024, 7, 1))
end_date = st.sidebar.date_input("End Date", datetime(2024, 8, 31))

# Ensure that the selected date range is valid
if start_date > end_date:
    st.sidebar.error("End Date must fall after Start Date")

# Retrieve data from InfluxDB
if st.sidebar.button("Retrieve AIS Data"):
    with st.spinner("Retrieving data..."):
        try:
            df = query_ais_data(start_date, end_date)
            st.success("Data retrieved successfully!")

            # Display raw data in a table
            st.subheader("AIS Data")
            st.dataframe(df)

            # Create a map using Plotly for lat/lon visualization
            st.subheader("AIS Vessel Locations")
            if not df.empty:
                # Plotly scattergeo plot for mapping lat/lon
                fig = px.scatter_geo(
                    df,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name="_time",
                    title="Vessel Locations",
                    projection="natural earth",
                )
                fig.update_geos(showcoastlines=True, coastlinecolor="Black", 
                                showland=True, landcolor="LightGreen",
                                showocean=True, oceancolor="LightBlue")

                st.plotly_chart(fig)
            else:
                st.warning("No data found for the selected date range.")
        except Exception as e:
            st.error(f"Error retrieving data: {e}")
