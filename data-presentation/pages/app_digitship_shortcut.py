import math
import re
from dataclasses import dataclass
import os
from os import listdir, getcwd
from os.path import isfile, join, isdir

import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import config
from navigation_data_analysis.imputation import impute
import navigation_data_analysis as nda
from navigation_data_analysis.imputation import Valid_Imputation
from navigation_data_analysis.prediction import Regression
from yellowbrick.cluster import KElbowVisualizer

COLUMNS = [
    "speed",              
    "course",          
    "heading",            
    "rot",                
    "draught",             
    "humidity",           
    "temperature",      
    "pressure",          
    "gust",                
    "windSpeed",         
    "windDir",
    "currentSpeed",
    'currentDir', 
    'priWaveDir', 
    'windWaveDir', 
    'waveSigH'
]

INPUT_PRED_COLUMNS = [
    "draught",             
    "humidity",           
    "temperature",      
    "pressure",          
    "gust",                
    "windSpeed",         
    "currentSpeed",
    'waveSigH'
]


@dataclass
class Options:
    SEASONS = ['spring', 'summer', 'fall', 'winter']
    SEASONS_RANGE = []
    OCEANS = ["North Atlantic Ocean", "South Atlantic Ocean", 'Arctic Ocean', 'Indian Ocean', 'North Pacific Ocean', 'South Pacific Ocean', 'Southern Ocean']


@dataclass
class UserInput:
    DIR_NAME: str
    FILE_NAME: str  # source csv file
    SRC_FILE_PATH: str
    NAVSTATUS: str
    OCEANS: list[str]
    SEASONS: int 
    NUM_OF_CLUSTERS: int
    IS_ELBOW: bool


@st.cache_data
def get_result_as_file(df):
    return df.to_csv().encode('utf-8')

@st.cache_data
def get_dataframe(url):
    return pd.read_csv(url)

def normalize(df: pd.DataFrame,
              method: str) -> pd.DataFrame:
    df = df.copy()
    if method == 'minmax':
        df = MinMaxScaler().fit_transform(df)
    elif method == 'cos':
        df = np.cos(np.radians(df))
    elif method == "sin":
        df = np.sin(np.radians(df))
    return df


def preprocess(df, standardize=False) -> pd.DataFrame:
    """ Preprocessing the dataset
    1. set index to be time
    2. select by name of columns
    3. remove outliers (discard)
    4. imputation
    5. standardization
    Args:
        df (Dataframe): Original dataset
        preserve_columns (list[str]): list columns of output
        standardize (Boolean): apply Standardization or not
    Returns:
        Dataframe: dataset after preprocessed
    """
    df = df.copy()
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp')
    # [detect outlier]
    # df = univariate_outlier_detection(df, method="Inner Fence")
    # [imputation]
    for (column, method) in config.imputation.items():
        if column in df: df.loc[:, column] = impute(df.loc[:, column], method)
    #df = df.reindex(sorted(df.columns), axis=1)
    if standardize: 
        for (column, method) in config.standardized_columns.items():
            if column in df: df.loc[:, column] = normalize(df[[column]], method) 
    return df


def elbow(df):
    # Instantiate the clustering model and visualizer
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(1, 12))

    visualizer.fit(df.to_numpy())   # Fit the data to the visualizer
    visualizer.finalize()
    # visualizer.show()   # Finalize and render the figure
    return plt.gcf()


def filter_by_season(df: pd.DataFrame, timestamp, seasons: list[str]) -> pd.DataFrame:
    months = []
    if 'winter' in seasons: months.extend([12,1,2])
    if 'summer' in seasons: months.extend([6,7,8])
    if 'spring' in seasons: months.extend([3,4,5])
    if 'fall' in seasons: months.append([9,10,11])
    return df[df.index.month.isin(months)]
     

def get_vessel_info(imo: int):
    vessels = pd.read_csv('./res/vessels_cut.csv')
    vessel = vessels[vessels.imo == imo]
    if len(vessel) > 0:
        return vessel.iloc[0].to_dict()
    return None


def build_sidebar_UI(DATA_DIR="/data/cleaned_files/") -> UserInput:
    """ At first, Build sidebar user interface and return the user defined values. """

    st.sidebar.subheader("Choose profile")
    dirs = [f for f in listdir(DATA_DIR) if isdir(
        join(DATA_DIR, f))]
    DIR_NAME = st.sidebar.selectbox("Select fleet", dirs, index=0)
    file = [f for f in listdir(join(DATA_DIR,DIR_NAME)) if isfile(
        join(DATA_DIR,DIR_NAME, f))]
    FILE_NAME = st.sidebar.selectbox("Select ship", file, index=0)
    SRC_FILE_PATH = join(DATA_DIR, DIR_NAME, FILE_NAME)
    df = get_dataframe(SRC_FILE_PATH)

    nav_status_list = df.navstatus.unique()
    NAVSTATUS = st.sidebar.multiselect(label="Select navigation status", options=nav_status_list, default=nav_status_list)
 
    df = df.dropna(subset=['ocean', 'sea'])
    oceansandseas = np.unique(np.concatenate((df['ocean'].unique(),df['sea'].unique()),0))
    if NAVSTATUS not in ['At anchor', 'Moored']:
        OCEANS = st.sidebar.multiselect(label='Select sailing area', options=oceansandseas, default=['Arabian Sea', 'Andaman or Burma Sea'])
        SEASONS = st.sidebar.multiselect(label='Select sailing time', options=['spring', 'summer', 'fall', 'winter'], default=['winter', 'summer', 'fall', 'winter'])
    else:
        OCEANS = oceansandseas
        SEASONS = Options.SEASONS

    st.sidebar.markdown("---")
    st.sidebar.subheader("Clustering")
    NUM_OF_CLUSTERS = st.sidebar.number_input("Set the number of cluster", value=3, min_value=1, max_value=20, step=1)
    clustering_method = st.sidebar.radio("Select clustering method", ['K-means', "Mean Shift"], horizontal=True)
    #reduce_dimention_method = st.sidebar.radio("Select dimension reduction technique", ['PCA', ])
    is_elbow = st.sidebar.checkbox(
        "Show Elbow method for analysis", value=False)

    return UserInput(
        DIR_NAME=DIR_NAME,
        FILE_NAME=FILE_NAME,
        SRC_FILE_PATH=SRC_FILE_PATH,
        NAVSTATUS=NAVSTATUS,
        OCEANS=OCEANS,
        SEASONS=SEASONS,
        NUM_OF_CLUSTERS=NUM_OF_CLUSTERS,
        IS_ELBOW=is_elbow
    )


def build_mainpage_result(ui: UserInput) -> None:
    #
    #   FILTERING
    #
    # preprocess -> filter
    # df_raw: from file
    # df_filtered: filted from df_raw
    # df_preprocessed: processed data from df_filtered
    df_raw = pd.read_csv(ui.SRC_FILE_PATH)
    timestamp = pd.to_datetime(df_raw["timestamp"])
    df_raw = df_raw.set_index(timestamp)
    df_preprocessed = preprocess(df_raw, standardize=False)

    df_filtered = df_preprocessed[df_preprocessed.navstatus.isin(ui.NAVSTATUS)]
    if 'ocean' in df_filtered: df_filtered = df_filtered[df_filtered['ocean'].isin(ui.OCEANS) | df_filtered['sea'].isin(ui.OCEANS)]
    df_filtered = filter_by_season(df_filtered, timestamp, ui.SEASONS)

    if not len(df_filtered.index):
        st.markdown("### Profile does not exist")
        return 0


    #
    #   SHIP INFORMATION
    # 
    imo = df_filtered.imo.array[0]
    vessel_info = get_vessel_info(imo)
    if vessel_info:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('#### Vessel: '+ vessel_info['name'])
            if vessel_info['gallery']: #TODO: fix error NaN value
                st.image(vessel_info['gallery'].split("'")[3])
        with col2:
            st.write("\n")
            st.write('IMO:\t '+ str(imo))
            st.write('Vessel type:\t ' + vessel_info['type_ship'])
            st.write('Length: ' + str(vessel_info['length']) + ' m')
            st.write('Breadth: ' + str(vessel_info['breadth']) + ' m')
            st.write('Deathweigh: '+ str(vessel_info['dwt']))
            st.write('Gross Tonnage: ' + str(vessel_info['gt']))
            st.write('Year built: '+ str(vessel_info['year_build']))
            st.write('Flag: ' + vessel_info['country_name'])

    st.markdown("### Data for this profile")
    st.write(df_filtered)
    st.write("Number of columns: ", format(len(df_filtered.columns)))
    st.write("Number of rows: {}".format(len(df_filtered)))


    #
    #   CLUSTERING
    #
    # clusters (list[DataFrame]): list of cluster0, cluster1...
    st.markdown("### Clustering")
    
    input_clustering_columns = st.multiselect("Input parameters of the clustering model", COLUMNS, ['speed'])
    input_pca_columns = st.multiselect("Input parameters for the dimension reduction model", COLUMNS, ['speed', 'currentSpeed', 'windSpeed'])

    df_clustering = df_filtered[input_clustering_columns].dropna()
    df_pca = df_filtered[input_pca_columns].dropna()

    if ui.IS_ELBOW:
        st.markdown("### Elbow Method")
        st.write('Elbow method is to detemine the number of clusters present in the data set')
        with st.empty():
            st.markdown("> Take some time to generate plot...")
            elbow_fig = elbow(df_clustering)
            st.write(elbow_fig)    

    X = df_clustering.to_numpy()
    kmeans = KMeans(n_clusters=ui.NUM_OF_CLUSTERS).fit(X)
    labels = kmeans.labels_

    clusters = [] # list of DFs
    for i in range(ui.NUM_OF_CLUSTERS):
        clusters.append(df_filtered[labels == i])

    st.markdown("#### Clustering result")
    st.write("after clustering + reducing dimension")
    pca = PCA(n_components=2)
    pca.fit(df_pca.to_numpy())

    pca_clusters = [] # [Dataframe(['x', 'y', 'cluster'])]
    df_clusters = [] # [pd.DataFrame()]
    for i in range(ui.NUM_OF_CLUSTERS):
        pca_clusters.append(pca.transform(df_pca.loc[clusters[i].index].to_numpy()))
        df_tmp = pd.DataFrame(data=pca_clusters[i], columns=["x", "y"])
        df_tmp["cluster"] = str(i)
        df_clusters.append(df_tmp)

    df_pxplot = pd.concat(df_clusters,
                            axis=0, ignore_index=True)
    fig = px.scatter(df_pxplot, x="x", y="y", color="cluster")
    st.write(fig)

    st.markdown("Center of each cluster:")
    clusters_info = pd.DataFrame(index=[i for i in range(ui.NUM_OF_CLUSTERS)], columns=COLUMNS, data=[clusters[i][COLUMNS].mean(axis=0) for i in range(ui.NUM_OF_CLUSTERS)])
    clusters_info['number of rows'] = pd.Series(data=[len(df_clusters[i]) for i in range(ui.NUM_OF_CLUSTERS)])
    clusters_info = clusters_info.rename_axis("cluster")
    st.write(clusters_info)
    #st.write(f"Clustering score (Silhouette): {metrics.silhouette_score(X, labels, metric='euclidean')}")

    st.markdown("#### Clusters on geography map")
    fig = go.Figure()
    fig.update_geos(resolution=110, #or 50
                    showcoastlines=True, coastlinecolor="RebeccaPurple",
                    showland=True, landcolor="whitesmoke",
                    showocean=True, oceancolor="LightBlue")
    for i in range(ui.NUM_OF_CLUSTERS):
        df_tmp = df_filtered[labels==i]
        #fig = px.scatter_geo(df_tmp, hover_data=['speed'], lat='lat', lon='lon', color_continuous_scale='red')
        fig.add_trace(go.Scattergeo(name=f'cluster {i}', 
                                    hovertext='Time: ' + df_tmp.index.astype(str) + '<br> Speed: ' + df_tmp.speed.astype(str) + '<br> Destination: ' +df_tmp.destination.astype(str), 
                                    lat=df_tmp.lat, 
                                    lon=df_tmp.lon, 
                                    mode='markers')
                                    )
    fig.update_layout(height=400, margin={"r":1,"t":8,"l":0,"b":0} )
    st.write(fig)
    
    st.sidebar.write("\n \n")
    if st.sidebar.button('Export profiles'): #, help="Files will be placed in 'output' folder"
        dir_main = getcwd()
        dir_name = ui.FILE_NAME[:-4] +'_' + '+'.join(ui.OCEANS)+'_' + '+'.join(ui.SEASONS)
        path = os.path.join(dir_main,'output', dir_name)
        try:
            os.mkdir(path)
        except OSError:
            pass

        fig.write_image(f'{dir_main}/output/{dir_name}/geo_map.jpg')
        df_filtered['cluster'] = labels
        df_filtered.to_csv(f'{dir_main}/output/{dir_name}/all_data.csv')
        clusters_info.to_csv(f'{dir_main}/output/{dir_name}/center_of_clusters.csv')
        st.sidebar.write(f'exported files to folder "{dir_main}/output/{dir_name}"')

    #
    #   PREDICTING
    #
    st.markdown("## Predicting")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Predicting")
    input_cluster_predicting = st.sidebar.radio("Input data from cluster", [f"cluster {i}" for i in range(ui.NUM_OF_CLUSTERS)] + ['all'], ui.NUM_OF_CLUSTERS)
    input_param_predicting = st.sidebar.multiselect("Choose input parameters", INPUT_PRED_COLUMNS, ['temperature', 'draught', 'humidity', 'windSpeed', 'currentSpeed'])
    target_predicting = st.sidebar.radio('Choose the target parameter', ['speed', 'power (TODO)'])

    df_predicting = clusters[0].loc[:, input_param_predicting + [target_predicting]]
    model, error, score, fig = Regression(df_predicting, target_predicting, 'Random Forest')
    st.write(fig)
    st.write("Error: ", error)
    st.write("Score: " , score)

    st.sidebar.button('Export predicting model')

    with st.expander("### Testing"):
        input = []
        for index, para in enumerate(input_param_predicting):
            input.append(st.number_input(
                f"{para:} 👇", 
                min_value=0.0, max_value=100.0,
                value=24.0
            ))
        result = model.predict([input])
        st.write(f"👉 Predicted {target_predicting}: {result.mean()}" )

    #make radar chart
    df_plot = df_filtered[['heading', 'windDir', 'windSpeed', 'currentDir', 'currentSpeed', 'speed','priWaveDir', 'windWaveDir', 'waveSigH', 'propeller speed service']]
    df_plot.reset_index(inplace=True, drop=True)
    df = df_plot

    with st.expander("Additional diagrams"):
        fig = get_line_polar_plot(df_plot)
        st.write(fig)

        
        waveSigH_bins = [0.1, 0.5, 1.25, 2.25, 4, 6, 9, 14]
        df['waveSigH_in_scale'] = pd.cut(df.waveSigH, bins=waveSigH_bins, labels=False, right=False)
        df['waveDir-heading'] = np.round(df['priWaveDir'] - df['heading'])
        df.loc[df['waveDir-heading'] < 0, 'waveDir-heading'] = df['waveDir-heading'] + 360
        df_by_delta = df.groupby(['waveDir-heading', 'waveSigH_in_scale']).agg(
            speed=('speed', 'mean'),
            waveSigH= ('waveSigH', 'mean'),
            frequency= ('waveSigH_in_scale', 'count')
        ).reset_index()
        fig = px.bar_polar(df_by_delta, r='speed', theta='waveDir-heading', color='waveSigH_in_scale', template="plotly_white",
                        color_discrete_sequence=px.colors.sequential.Darkmint_r
                        )    
        fig.add_layout_image(
            dict(
                source="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Japanese_Map_symbol_%28Other_Ferry%29.svg/250px-Japanese_Map_symbol_%28Other_Ferry%29.svg.png",
                x=0.5, y=0.5,
                xanchor="center",
                yanchor="middle",
                sizex=0.1,
                sizey=0.1,
                opacity=0.3
            )
        )
        fig.update_layout(
            polar={"angularaxis":{"dtick":45/2}},
            title='Vessel speed vs Wave height'    
        )
        st.write(fig)
        



        wind_speed_bins = [1,3,7,12,18,24,31,38,46,54,63,72]
        df['wind_speed_in_scale'] = pd.cut(df.windSpeed, bins=wind_speed_bins, labels=False, right=False)
        df['delta_windDir'] = np.round(df['windDir'] - df['heading'])
        df.loc[df['delta_windDir'] < 0, 'delta_windDir'] = df['delta_windDir'] + 360
        df_by_delta = df.groupby(['delta_windDir', 'wind_speed_in_scale']).agg(
            speed=('speed', 'mean'),
            windSpeed= ('windSpeed', 'mean'),
            frequency= ('wind_speed_in_scale', 'count')
        ).reset_index()
        fig = px.bar_polar(df_by_delta, r='speed', theta="delta_windDir", color='wind_speed_in_scale', template="plotly_white",
                        color_discrete_sequence=px.colors.sequential.Brwnyl_r
                        )    
        fig.add_layout_image(
            dict(
                source="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Japanese_Map_symbol_%28Other_Ferry%29.svg/250px-Japanese_Map_symbol_%28Other_Ferry%29.svg.png",
                x=0.5, y=0.5,
                xanchor="center",
                yanchor="middle",
                sizex=0.1,
                sizey=0.1,
                opacity=0.3
            )
        )
        fig.add_layout_image(
            dict(
                source="https://i.ibb.co/F87KLtG/wind-icon.jpg",
                x=0.5, y=-0.1,
                xanchor="center",
                yanchor="middle",
                sizex=0.1,
                sizey=0.1,
                opacity=1
            )
        )
        fig.add_layout_image(
            dict(
                source="https://i.postimg.cc/FKVBTD8M/wind-go-up.jpg",
                x=0.5, y=1.1,
                xanchor="center",
                yanchor="middle",
                sizex=0.1,
                sizey=0.1,
                opacity=1
            )
        )
        fig.update_layout(
            polar={"angularaxis":{"dtick":45/2}},
            #showlegend=True,
            title='Vessel speed vs Wind speed'
        )
        st.write(fig)


        currentSpeed_bins = [0.1, 0.2, 0.4, 0.6, 0.8, 1, 1.2]
        df['currentSpeed_in_scale'] = pd.cut(df.currentSpeed, bins=currentSpeed_bins, labels=False, right=False)
        df['currentDir-heading'] =  np.round(df['currentDir'] - df['heading'])
        df.loc[df['currentDir-heading'] < 0, 'currentDir-heading'] = df['currentDir-heading'] + 360
        #if delta_theta < 0 : delta_theta = 360-delta_theta
        df_by_delta = df.groupby(['currentDir-heading', 'currentSpeed_in_scale']).agg(
            speed=('speed', 'mean'),
            windSpeed= ('windSpeed', 'mean'),
            currentSpeed = ('currentSpeed', 'mean'),
            frequency= ('currentSpeed_in_scale', 'count')
        ).reset_index()
        fig = px.bar_polar(df_by_delta, r='speed', theta='currentDir-heading', color='frequency', template="plotly_white",
                        color_discrete_sequence=px.colors.sequential.Brwnyl_r
                        )    
        fig.add_layout_image(
            dict(
                source="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Japanese_Map_symbol_%28Other_Ferry%29.svg/250px-Japanese_Map_symbol_%28Other_Ferry%29.svg.png",
                x=0.5, y=0.5,
                xanchor="center",
                yanchor="middle",
                sizex=0.1,
                sizey=0.1,
                opacity=0.3
            )
        )
        fig.update_layout(
            polar={"angularaxis":{"dtick":45/2}},
            title='Vessel speed vs Current speed'
        )
        st.write(fig)
    

def get_line_polar_plot(df):
    angle_range = [(-3,6)]+ [(i, i+6) for i in range(0,360,6)] + [(357, 361)]
    def assign_degree(heading):     
        for start, end in angle_range:
            if start <= heading < end:
                return start+3
        return 0
    df['heading-windDir'] = df['heading'] - df['windDir']
    df.loc[df['heading-windDir'] < 0, 'heading-windDir'] = df['heading-windDir'] + 360
    df['heading-windDir'] = df['heading-windDir'].apply(assign_degree)

    df_by_delta = df.groupby(['heading-windDir']).agg(
        speed=('speed', 'mean'),
        currentSpeed= ('currentSpeed', 'mean'),
        windSpeed= ('windSpeed', 'mean'),
    )

    angles = df_by_delta.index   # = [0, 45, 90, 135, 180, 225, 270, 315]
    speed_over_ground = df_by_delta.speed       #= [8, 12, 18, 22, 28, 32, 38, 42]
    windSpeed = df_by_delta.windSpeed    # = [10, 15, 20, 25, 30, 35, 40, 45]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=speed_over_ground,
        theta=angles,
        mode='lines',
        #width=15,
        marker_color='red',
        name='Speed'
    ))

    fig.add_layout_image(
        dict(
            source="https://i.ibb.co/F87KLtG/wind-icon.jpg",
            x=0.5, y=1.1,
            xanchor="center",
            yanchor="middle",
            sizex=0.1,
            sizey=0.1,
            opacity=1
        )
    )

    fig.update_layout(
        title='Vessel heading results in Speed over Ground',
        polar=dict(
            angularaxis=dict(
                direction='clockwise'
            ),
            radialaxis=dict(
                visible=True,
                range=[0, max(windSpeed + speed_over_ground) + 40],
            ),
        ),
        showlegend=True,
    )
    return fig

        
def main():
    st.set_page_config(
        page_title="Operation Profile Application",
        page_icon="chart_with_upwards_trend",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)
    user_input = build_sidebar_UI()
    build_mainpage_result(user_input)


if __name__ == "__main__":
    main()
