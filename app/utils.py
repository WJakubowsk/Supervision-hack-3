import os
import pdfplumber
import easyocr
import numpy as np
import streamlit as st
from typing import List
from difflib import Differ, SequenceMatcher

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

def calculate_similarity_ratio_between_strings(first_text: str, second_text: str) -> str:
    """
    Calculates how two strings are similar to each other using the employs an algorithm 
    based on the Ratcliff/Obershelp algorithm.
    Returns the percentage value from range [0, 100] when 0% denotes no similarity at all 
    and 100% denotes the identical similarity.
    """
    return 100 * round(SequenceMatcher(None, first_text, second_text).ratio(), 3)

def compare_strings(first_text: str, second_text: str) -> str:
    """
    Compares two texts (like two versions of SCFR files from different years).
    Returns a string with the pointers emphasising the varying places in both text.
    """
    d = Differ()
    diff = list(d.compare(first_text.splitlines(), second_text.splitlines()))
    # diff_text = '\n'.join(diff)
    return diff

def _extract_text_from_page(page: pdfplumber.page) -> str:
    """
    Extracts text from given page.
    """
    return page.extract_text()

def _perform_ocr_on_page(page: pdfplumber.page) -> str:
    """
    Performs OCR on the page scan.
    """
    reader = easyocr.Reader(['pl'])
    img_np = np.array(page.to_image().original)
    result = reader.readtext(img_np)
    return ' '.join([res[1] for res in result])

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file. If the PDF contains scans instead of machine-encoded text,
    conversion to images and OCR is utilized.
    Returns text in one string.
    """

    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text_from_page = _extract_text_from_page(page)
            text += text_from_page if text_from_page else _perform_ocr_on_page(page) + '\n'

    return text

def color_line(line: str) -> str:
    """
    Applies coloring the lines which are being different in two files.
    """
    if line.startswith('-'):
        return f'<span style="color: blue;">{line}</span>'
    elif line.startswith('+'):
        return f'<span style="color: green;">{line}</span>'
    else:
        return line