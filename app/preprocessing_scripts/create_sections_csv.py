import fitz 
import re
import pandas as pd
import re
import os
from typing import List

additional_strings = [
    'A Działalność i wyniki operacyjne',
    'A.1 Działalność',
    'A.2 Wynik z działalności ubezpieczeniowej',
    'A.3 Wynik z działalności lokacyjnej (inwestycyjnej)',
    'A.4 Wyniki z pozostałych rodzajów działalności',
    'A.5 Wszelkie inne informacje',
    'B System zarządzania',
    'B.1 Informacje ogólne o systemie zarządzania',
    'B.2 Wymogi dotyczące kompetencji i reputacji',
    'B.3 System zarządzania ryzykiem, w tym własna ocena ryzyka i wypłacalności',
    'B.4 System kontroli wewnętrznej',
    'B.5 Funkcja audytu wewnętrznego',
    'B.6 Funkcja aktuarialna',
    'B.7 Outsourcing',
    'B.8 Wszelkie inne informacje',
    'C Profil ryzyka',
    'C.1 Ryzyko aktuarialne',
    'C.2 Ryzyko rynkowe',
    'C.3 Ryzyko kredytowe',
    'C.4 Ryzyko płynności',
    'C.5 Ryzyko operacyjne',
    'C.6 Pozostałe istotne ryzyka',
    'C.7 Wszelkie inne informacje',
    'D Wycena do celów wypłacalności',
    'D.1 Aktywa',
    'D.2 Rezerwy techniczno-ubezpieczeniowe',
    'D.3 Inne zobowiązania',
    'D.4 Alternatywne metody wyceny',
    'D.5 Wszelkie inne informacje',
    'E Zarządzanie kapitałem',
    'E.1 Środki własne',
    'E.2 Kapitałowy wymóg wypłacalności i minimalny wymóg kapitałowy',
    'E.3 Zastosowanie podmodułu ryzyka cen akcji opartego na duracji do obliczenia kapitałowego wymogu wypłacalności',
    'E.4 Różnice między formułą standardową, a stosowanym modelem wewnętrznym',
    'E.5 Niezgodność z minimalnym wymogiem kapitałowym i niezgodność z kapitałowym wymogiem wypłacalności',
    'E.6 Wszelkie inne informacje',
]



def extract_variables_from_filename(filename:str):
    """
    Extracts the year, LEI code and name of the company from the filename.
    """
    pattern = re.compile(r'(\d{4})_SFCR_(\w{20})_(.+)\.pdf')
    match = pattern.match(filename)

    if match:
        rok = int(match.group(1))
        kodLEI = match.group(2)
        nazwa = match.group(3)
        return rok, kodLEI, nazwa
    else:
        raise ValueError("Filename does not match the expected format.")

def create_additional_df():
    """
    Creates a DataFrame from the additional_strings list.
    """
    data = []
    for string in additional_strings:
        code, name = string.split(' ', 1)
        data.append({'Section Code': code.strip(), 'Section Name': name.strip()})
    return pd.DataFrame(data)

def extract_text_from_pdf(pdf_path):
    """
    Extracts the text from the PDF file to one string.
    """
    text = ""
    doc = fitz.open(pdf_path)

    for page_num in range(2, doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    text = re.sub(r'\s+', ' ', text)
    return text

def create_section_df(sections_list, text, sections_ids_path):
    """
    Creates a DataFrame with the sections and their content.
    """
    sections_list.insert(0, "Podsumowanie")
    rows = []
    for section_name in sections_list:
        content = extract_content(section_name, text, sections_list)
        if section_name == 'Podsumowanie':
            section_code = ''
            rows.append({'Section Code': 'Podsumowanie' , 'Section Content': content, 'Section Name': ''})
            continue
        if section_name in additional_strings:
            section_code = ''
            rows.append({'Section Code': section_name.strip(), 'Section Content': content, 'Section Name': section_code})
        else:
            section_code = extract_substring(content)
            section_code = section_code[:-1]
            content = content[len(section_code):]
            rows.append({'Section Code': section_name.strip() + ' ' + section_code, 'Section Content': content, 'Section Name': section_code})

    df = pd.DataFrame(rows, columns=['Section Code', 'Section Name', 'Section Content'])
    df.rename(columns={'Section Code': 'NAZWA_Sekcji','Section Content':'treść'},inplace=True)
    sections_ids_df= pd.read_csv(sections_ids_path, sep=';')
    merged_df = pd.merge(df, sections_ids_df, left_on='NAZWA_Sekcji', right_on='Nazwa Sekcji (według Rozporządzenia)', how='left')
    merged_df.drop(columns=['Nazwa Sekcji (według Rozporządzenia)', 'Section Name'], inplace=True)
    return merged_df

def find_unique_strings(text: str, df: pd.DataFrame):
    """
    Find subsubsections in the text.
    """
    additional_sections = list(df['Section Code'])
    pattern1 = r'[A-E]\.\d+\.\d'
    pattern2 = r'[A-E]\.\d+\.\d+\.\d'
    pattern3 = r'[A-E]\.\d'
    pattern4 = r'[A-E]'

    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)
    matches3 = re.findall(pattern3, text)
    matches4 = re.findall(pattern4, text)
    matches = matches1 + matches2 + matches3 + matches4

    unique_strings = set(matches)
    unique_strings = unique_strings.union(set(additional_sections))
    sorted_items = sorted(list(unique_strings), key=lambda x: (x[0], int(x.split('.')[1]) if len(x.split('.')) > 1 and x.split('.')[1] else 0, int(x.split('.')[2]) if len(x.split('.')) > 2 and x.split('.')[2] else 0))
    for i, item in enumerate(sorted_items):
        for additional_item in additional_strings:
            if item.strip() == additional_item.split()[0].strip():
                sorted_items[i] = additional_item
                break
    
    return sorted_items


def extract_content(section_name: str, text: str, sections_list: List[str]):
    """
    Extracts the content of the section from the text.
    """
    start_idx = text.find(section_name)
    next_section_index = sections_list.index(section_name) + 1 if section_name in sections_list[:-1] else None
    end_section = sections_list[next_section_index] if next_section_index is not None else None
    end_idx = text.find(end_section) if end_section is not None else len(text)

    if start_idx != -1 and end_idx != -1:
        return text[start_idx + len(section_name):end_idx].strip()
    elif start_idx != -1:
        return text[start_idx + len(section_name):].strip()
    else:
        return ''

def extract_substring(s):
    """
    Extracts the substring from the beginning of the string.
    """
    result = ""
    for i, char in enumerate(s):
        if i > 0 and char.isupper():
            break
        result += char
    return result


def fulfill_df(merged_df, rok, kodLEI):
    """
    Add missing columns and fill NaN values.
    """
    start_value = 38
    increment = 1
    for index, row in merged_df.iterrows():
        if pd.isna(row['ID SekcjI (stała)']):
            merged_df.at[index, 'ID SekcjI (stała)'] = start_value
            start_value += increment
    merged_df['ID SekcjI (stała)'] = merged_df['ID SekcjI (stała)'].astype('Int64')
    for index, row in merged_df.iterrows():
        if pd.isna(row['id sekcji nadrzędnej (Stała)']):
            first_three_letters = row['NAZWA_Sekcji'][:3]
            matching_row = merged_df[merged_df['NAZWA_Sekcji'].str.startswith(first_three_letters)].iloc[0]
            merged_df.at[index, 'id sekcji nadrzędnej (Stała)'] = matching_row['ID SekcjI (stała)']

    merged_df['id sekcji nadrzędnej (Stała)'][0] = 1
    merged_df['ID_TAB'] = 1
    merged_df['data SFCR']=rok
    merged_df['wersja SFCR']=1
    merged_df['numer zakładu w systemie UKNF (kod zakładu)'] = kodLEI
    return merged_df




def main():
    filename = "2023_SFCR_259400B0G3LJVFVZS942_NATIONALE-NEDERLANDEN TUnŻ S.A..pdf"
    section_ids_path = "data/sekcje.csv"
    pdf_path = os.path.join("data", filename)
    rok, kodLEI, nazwa = extract_variables_from_filename(filename)
    df_additional = create_additional_df()
    text = extract_text_from_pdf(pdf_path)
    old_str = find_unique_strings(text, df_additional)
    merged_df = create_section_df(old_str, text, section_ids_path)
    merged_df = fulfill_df(merged_df, rok, kodLEI)
    print(merged_df)
    merged_df.to_csv("data/sections_df.csv")

if __name__ == '__main__':
    main()