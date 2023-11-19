import streamlit as st
import pandas as pd
from utils import *
from preprocessing_scripts.completness_check import check_completness
from preprocessing_scripts.create_sections_csv_advanced import find_unique_strings, create_section_df
from preprocessing_scripts.find_tables_in_document import check_if_table_in_document, get_all_tables, required_rows_dict
from scraper import scraper
import os
from pathlib import Path
import pickle

# for demo only, removes unnucessary elements from the app:
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)


PATH = Path(__file__)
ZAKLADY_PATH = PATH.parent.parent / 'data' / 'zaklady.csv'
SFCR_PATH = PATH.parent.parent / 'data' / 'sfcr'
SEKCJE_PATH = PATH.parent.parent / 'data' / 'sekcje.csv'
DANE_JAKOSCIOWE = PATH.parent.parent / 'data' / 'dane_jakosciowe.csv'

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
            folder_path = st.sidebar.text_input('Enter local path to directory with files for analysis', './')
            select_all_files = st.sidebar.checkbox("Select all files")
            selected_files = file_selector(folder_path, select_all_files)
            st.sidebar.header('Destination directory for CSV files')
            destination_folder_path = st.sidebar.text_input('Enter local path to directory where the processed CSV files should be saved', '.')

        if st.sidebar.button('Divide the selected SFCR documents into sections'):
            for filename in selected_files:
                pdf_path = os.path.join(PATH.parent.parent, "data", "sfcr", company, filename)
                text = extract_text_from_pdf(pdf_path)
                sections = list(find_unique_strings(text))
                sections.sort()
                merged_df = create_section_df(text, sections, filename, SEKCJE_PATH)
                merged_df.to_csv(destination_folder_path +  filename + '/sections.csv', index=False, sep=';')

        if st.sidebar.button('Check completness of the sections'):
            df = pd.read_csv(DANE_JAKOSCIOWE)
            df_completness = check_completness(df)
            df_completness.to_csv(destination_folder_path + filename + '/completness.csv', index = False)

        if st.sidebar.button('Extract tables from the SFCR file'):
            # for filename in selected_files:
            #     pdf_path = os.path.join("data", filename)
            #     tables = get_all_tables(pdf_path)
            #     for table in tables:
            #         table_present, table_parts, present_rows, all_cols_present = check_if_table_in_document(tables,table)
            #         st.markdown(f"Is table present: {table_present}")
            #         st.markdown("present_rows: ", present_rows)
            #         st.markdown("Are all columns present? ", all_cols_present)
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
