import streamlit as st
import os
from utils import *


def main():
    st.title('Supervision hack #SF_CRacker app')

    st.sidebar.title('Filters')

    st.sidebar.header('Files to download')
    folder_path = st.sidebar.text_input('Enter local path to files for analysis', '.')

    select_all_files = st.sidebar.checkbox("Select all files")
    selected_files = file_selector(folder_path, select_all_files)

    st.write('### Selected files:')
    st.write(selected_files)

    # Tu można dodać kod do analizy lub porównania wybranych plików

if __name__ == '__main__':
    main()