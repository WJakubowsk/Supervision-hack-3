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

    # podziel na sekcje

    # sprawdz kompletnosc sekcji

    # wyciagnij tabele z pliku

    if st.checkbox('Compare Texts from two files:'):
        try:
            # Input for file paths
            uploaded_file1 = st.file_uploader('Upload first file:', type=['pdf'])
            uploaded_file2 = st.file_uploader('Upload second file:', type=['pdf'])

            text_file1 = extract_text_from_pdf(uploaded_file1)
            text_file2 = extract_text_from_pdf(uploaded_file2)

            differences = compare_strings(text_file1, text_file2)
            colored_lines = [color_line(line) for line in differences]
            st.markdown(f'Estimated similarity between two files: {calculate_similarity_ratio_between_strings(text_file1, text_file2)}%.')
            st.markdown(f'### Differences:')
            for line in colored_lines:
                st.markdown(line, unsafe_allow_html=True)
        except Exception as e:
            st.markdown('Waiting for input..')

if __name__ == '__main__':
    main()