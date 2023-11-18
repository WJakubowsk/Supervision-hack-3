import os
import streamlit as st
from typing import List

def file_selector(folder_path: str = '.', select_all: bool = False) -> List[str]:
    """
    Module for selecting files from the given local path.
    """
    filenames = os.listdir(folder_path)
    if select_all:
        selected_files = st.multiselect('Select files', filenames, default=filenames)
    else:
        selected_files = st.multiselect('Select files', filenames)
    return selected_files

def count_selected_files(selected_files: List[str]) -> int:
    """
    Returns a number of selected files for analysis in the app.
    """
    return len(selected_files)