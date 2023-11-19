import sys
sys.settrace
import numpy as np
import pandas as pd
import pdfplumber
import easyocr
import transformers
from typing import List

SEARCH_TERMS = ['opinia z zastrzeżeniem', 'opinia z zastrzeżeniami', 'podstawa opinii z zastrzeżeniem',
                'opinia negatywna', 'podstawa opinii negatywnej', 'odmowa wyrażenia opinii']

QA_PIPELINE = transformers.pipeline(
    "question-answering",
    model="henryk/bert-base-multilingual-cased-finetuned-polish-squad1",
    tokenizer="henryk/bert-base-multilingual-cased-finetuned-polish-squad1"
)

# QA_PIPELINE = transformers.pipeline(
#     "question-answering",
#     model="dkleczek/bert-base-polish-cased-v1",
#     tokenizer="dkleczek/bert-base-polish-cased-v1"
# )

# def extract_text_from_pdf(pdf_path: str) -> str:
#     """
#     Extracts text from pdf file. If pdf contains scans instead of machine-encoded text, 
#     conversion to images and OCR is utilized.
#     Returns text in one string.
#     """
#     with pdfplumber.open(pdf_path) as pdf:
#         text = ''
#         for page in pdf.pages:
#             text += page.extract_text()
        
#         # if there is no text, the review is probably a scan, hence OCR
#         if text == '':
#             reader = easyocr.Reader(['pl'])
#             for page in tqdm(pdf.pages):
#                 img_np = np.array(page.to_image().original)
#                 result = reader.readtext(img_np)
#                 extracted_text = ' '.join([res[1] for res in result])
#                 text += extracted_text + '\n'
#         return text
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

def get_review_issue_date(text: str, qa_pipeline: transformers.pipeline = QA_PIPELINE) -> str:
     """
     Returns the date the review has been issued by the auditor.
     The date is extracted using the BERT model, finetuned to polish use-case.
     """
     return qa_pipeline({'context': f"{text}", 'question': "Jaka jest data podpisania dokumentu?"}).get('answer')

def get_auditors_review_outcome(text: str, search_terms: List[str] = SEARCH_TERMS) -> bool:
    """
    Returns the outcome of the auditor's review - whether there were any disclaimers or not.
  
    """
    return True if any(term in text for term in search_terms) else False

def main():
    pdf_file = input('Enter path to pdf auditor\'s review file:')
    text = extract_text_from_pdf(pdf_file)
    print("date of review:", get_review_issue_date(text))
    print("Review contains disclaimers and/or is negative:", get_auditors_review_outcome(text))

if __name__ == '__main__':
    main()