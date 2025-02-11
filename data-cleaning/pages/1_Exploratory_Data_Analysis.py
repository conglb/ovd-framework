import streamlit as st
import pandas as pd
import os
import io
import io
from os import listdir
from dataclasses import dataclass
from os.path import join, isdir, isfile
from utlis import get_file_list, get_folder_list, get_cleaning_scripts, SCRIPT_FILES_DIR, CLEANED_FILES_DIR, RAW_FILES_DIR, list_files_in_directory
import plotly.express as px
import plotly.express as px




@dataclass
class UserInput:
    DIR_NAME: str
    FILE_NAME: str  
    SRC_FILE_PATH: str

@st.cache_data
def get_dataframe(url):
    return pd.read_csv(url)

def build_sidebar_UI(DATA_DIR="../data/raw_files") -> UserInput:
    """ At first, Build sidebar user interface and return the user defined values. """

    st.sidebar.subheader("Choose data file")
    dirs = [f for f in listdir(DATA_DIR) if isdir(
        join(DATA_DIR, f))]
    DIR_NAME = st.sidebar.selectbox("Select data folder", dirs, index=0)
    file = [f for f in listdir(join(DATA_DIR,DIR_NAME)) if isfile(
        join(DATA_DIR,DIR_NAME, f))]
    FILE_NAME = st.sidebar.selectbox("Select data file", file, index=0)
    SRC_FILE_PATH = join(DATA_DIR, DIR_NAME, FILE_NAME)


    return UserInput(
        DIR_NAME=DIR_NAME,
        FILE_NAME=FILE_NAME,
        SRC_FILE_PATH=SRC_FILE_PATH,
    )

def build_main_UI(user_input: UserInput) -> None:

    df = get_dataframe(user_input.SRC_FILE_PATH)
    st.write(df)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Number of columns: ", len(df.columns) )
        colume_name = st.selectbox('Choose colume', df.columns)
        data_type = df[colume_name].dtype
        st.write("Column's data type: ",data_type)
        st.write("Number of rows: ", len(df))
        st.write("Number of NaN values: ",df[colume_name].isna().sum())
        st.write("Number of Not-Null values: ",df[colume_name].notna().sum())
        if data_type != object:
            st.write("Min: ",df[colume_name].min())
            st.write("Max: ",df[colume_name].max())
            st.write("Mean: ",df[colume_name].mean())
        else:
            st.write(f"Number of unique values: ", len(df[colume_name].unique()))
    with col2:
        if data_type == object:
            unique_values = df[colume_name].unique()
            st.write(", ".join(map(str, unique_values)))
        else:
            fig = px.histogram(df[colume_name], marginal="box", barmode="group")
            fig.update_layout(
                title_text="Histogram of the Column",
                title_x=0.5,
                yaxis_title="# of entries",
                xaxis_title="Value")
            st.write(fig)
            


# Streamlit App def main():
st.set_page_config(
        page_title="Explore Data",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/conglb',
            'Report a bug': "https://github.com/conglb",
        }
    )
user_input = build_sidebar_UI()
build_main_UI(user_input)
