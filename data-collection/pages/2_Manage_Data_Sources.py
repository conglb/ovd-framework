import streamlit as st
import pandas as pd
from utils import load_data_sources, delete_data_source, edit_data_source

st.title("Manage Data Sources")

# Load and display data sources
data_sources = load_data_sources()
if len(data_sources) == 0:
    st.warning("No data sources available.")
else:
    df = pd.DataFrame(data_sources)
    st.dataframe(df)

    # Option to delete or edit a data source
    st.write("### Delete or Edit a Data Source")
    index_to_delete = st.number_input("Select the index of the source to delete", min_value=0, max_value=len(data_sources) - 1, step=1)

    if st.button("Delete Source"):
        delete_data_source(index_to_delete)
        st.success("Data source deleted.")
        st.experimental_rerun()

    # Editing an existing data source
    st.write("### Edit a Data Source")
    index_to_edit = st.number_input("Select the index of the source to edit", min_value=0, max_value=len(data_sources) - 1, step=1)

    if st.checkbox("Edit this source"):
        edited_name = st.text_input("Edit Name", value=data_sources[index_to_edit]["name"])
        edited_url = st.text_input("Edit URL", value=data_sources[index_to_edit]["url"])
        edited_description = st.text_area("Edit Description", value=data_sources[index_to_edit]["description"])

        if st.button("Save Changes"):
            edit_data_source(index_to_edit, edited_name, edited_url, edited_description)
            st.success("Data source updated.")
            st.experimental_rerun()