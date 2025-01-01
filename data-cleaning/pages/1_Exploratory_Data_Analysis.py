import streamlit as st
import pandas as pd
import os
import io
from os import listdir
from dataclasses import dataclass
from os.path import join, isdir, isfile
from utlis import get_file_list, get_folder_list, get_cleaning_scripts, SCRIPT_FILES_DIR, CLEANED_FILES_DIR, RAW_FILES_DIR, list_files_in_directory




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

    colume_name = st.selectbox('Choose colume', df.columns)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(df[colume_name].describe())
    
    buffer = io.StringIO()
    df.info(buf=buffer, verbose=True)
    s = buffer.getvalue()
    st.text(s)


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
