import streamlit as st
import pandas as pd
from utils import *
from preprocessing_scripts.completness_check import check_completness
from preprocessing_scripts.create_sections_csv_advanced import find_unique_strings, create_section_df
from scraper import scraper
import os

def main():
    try:
        file_path = os.path.abspath('../data/zaklady.csv')
        insurance_companies = pd.read_csv(file_path, sep=';')
    except:
        st.text('File not found in specified directory, try again.')
    else:
        st.title('#supervision_hack 3 - #SF_CRacker')

        st.markdown('### Picipolo')

        st.sidebar.title('Options')

        company = st.selectbox('Choose insurance company', insurance_companies['NAZWA ZAKŁADU'])
        scrape_button = st.button("Scrape SCFR documents for selected company")
        if scrape_button:
            with st.spinner('Scraping...'):
                scraper.run(destination_dir='./data/sfcr/', df=insurance_companies, company=company)

        st.sidebar.header('Source directory with SFCR files')
        folder_path = st.sidebar.text_input('Enter local path to directory with files for analysis', '.')
        select_all_files = st.sidebar.checkbox("Select all files")
        selected_files = file_selector(folder_path, select_all_files)

        st.sidebar.header('Destination directory for CSV files')
        destination_folder_path = st.sidebar.text_input('Enter local path to directory where the processed CSV files should be saved', '.')

        if st.sidebar.button('Divide the SFCR documents into sections'):
            filename = "2023_SFCR_259400IBCICD0KY7ZW46_TU ALLIANZ ŻYCIE POLSKA S.A..pdf" # example, provide pdf file name of your choice
            pdf_path = os.path.join("data", filename)
            text = extract_text_from_pdf(pdf_path)
            sections = find_unique_strings(text)
            sections = list(sections)
            sections.sort()
            merged_df = create_section_df(text, sections, filename)
            merged_df.to_csv('data/sections.csv', index=False, sep=';')
            pass

        if st.sidebar.button('Check completness of the sections'):
            df = pd.read_csv('../data/dane_jakosciowe.csv', index = False)
            df_completness = check_completness(df)
            df_completness.to_csv(destination_folder_path, index = False)

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
