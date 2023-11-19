import streamlit as st
import pandas as pd
from utils import *
from preprocessing_scripts.completness_check import check_completness
from scraper import scraper
import os
from pathlib import Path

PATH = Path(__file__)
ZAKLADY_PATH = PATH.parent.parent / 'data' / 'zaklady.csv'
SFCR_PATH = PATH.parent.parent / 'data' / 'sfcr'

def main():
    try:
        insurance_companies = pd.read_csv(ZAKLADY_PATH, sep=';')
    except:
        st.text('File not found in specified directory, try again.')
    else:
        st.title('#supervision_hack 3 - #SF_CRacker')

        st.markdown('### Picipolo')

        st.sidebar.title('Options')

        company = st.selectbox('Choose insurance company', insurance_companies['NAZWA ZAKŁADU'])
        scrape_button = st.button("Scrape SCFR documents for selected company")
        try:
            if scrape_button:
                with st.spinner('Scraping...'):
                        scraper.run(destination_dir=SFCR_PATH, df=insurance_companies, company=company)
        except Exception as e:
            st.error('Error during scraping, try again.')
        else:
            st.sidebar.header('Source directory with SFCR files')
            folder_path = st.sidebar.text_input('Enter local path to directory with files for analysis', '.')
            select_all_files = st.sidebar.checkbox("Select all files")
            selected_files = file_selector(folder_path, select_all_files)

            st.sidebar.header('Destination directory for CSV files')
            destination_folder_path = st.sidebar.text_input('Enter local path to directory where the processed CSV files should be saved', '.')

            if st.sidebar.button('Divide the SFCR documents into sections'):
                #TODO add podzial na sekcje
                pass

            if st.sidebar.button('Check completness of the sections'):
                df = pd.read_csv('../data/dane_jakosciowe.csv', index = False)
                df_completness = check_completness(df)
                pass

            if st.sidebar.button('Extract tables from the file'):
                #TODO add wyciagnac tabele z pliku
                pass

            if st.sidebar.checkbox('Compare texts from two files'):
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
