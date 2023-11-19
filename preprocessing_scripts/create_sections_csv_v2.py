import fitz 
import pandas as pd
import re
import os

additional_strings = [
    'A. Działalność i wyniki operacyjne',
    'A.1 Działalność',
    'A.2 Wynik z działalności ubezpieczeniowej',
    'A.3 Wynik z działalności lokacyjnej (inwestycyjnej)',
    'A.4 Wyniki z pozostałych rodzajów działalności',
    'A.5 Wszelkie inne informacje',
    'B. System zarządzania',
    'B.1 Informacje ogólne o systemie zarządzania',
    'B.2 Wymogi dotyczące kompetencji i reputacji',
    'B.3 System zarządzania ryzykiem, w tym własna ocena ryzyka i wypłacalności',
    'B.4 System kontroli wewnętrznej',
    'B.5 Funkcja audytu wewnętrznego',
    'B.6 Funkcja aktuarialna',
    'B.7 Outsourcing',
    'B.8 Wszelkie inne informacje',
    'C. Profil ryzyka',
    'C.1 Ryzyko aktuarialne',
    'C.2 Ryzyko rynkowe',
    'C.3 Ryzyko kredytowe',
    'C.4 Ryzyko płynności',
    'C.5 Ryzyko operacyjne',
    'C.6 Pozostałe istotne ryzyka',
    'C.7 Wszelkie inne informacje',
    'D. Wycena do celów wypłacalności',
    'D.1 Aktywa',
    'D.2 Rezerwy techniczno-ubezpieczeniowe',
    'D.3 Inne zobowiązania',
    'D.4 Alternatywne metody wyceny',
    'D.5 Wszelkie inne informacje',
    'E. Zarządzanie kapitałem',
    'E.1 Środki własne',
    'E.2 Kapitałowy wymóg wypłacalności i minimalny wymóg kapitałowy',
    'E.3 Zastosowanie podmodułu ryzyka cen akcji opartego na duracji do obliczenia kapitałowego wymogu wypłacalności',
    'E.4 Różnice między formułą standardową, a stosowanym modelem wewnętrznym',
    'E.5 Niezgodność z minimalnym wymogiem kapitałowym i niezgodność z kapitałowym wymogiem wypłacalności',
    'E.6 Wszelkie inne informacje',
]

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
    text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(5, doc.page_count):
        page = doc[page_num]
        text += page.get_text()

    return text

def find_unique_strings(text):
    """
    Find subsubsections in the text.
    """
    pattern1 = r'[A-E]\.\d+\.\d'
    pattern2 = r'[A-E]\.\d+\.\d+\.\d'
    pattern3 = r'[A-E]\.\d'
    pattern4 = r'[A-E]\.'

    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)
    matches3 = re.findall(pattern3, text)
    matches4 = re.findall(pattern4, text)
    matches = matches1 + matches2 + matches3 + matches4
    unique_strings = set(matches)
    return unique_strings

def create_additional_df():
    """
    Creates a DataFrame from the additional_strings list.
    """
    data = []
    for string in additional_strings:
        code, name = string.split(' ', 1)
        data.append({'Section Code': code.strip(), 'Section Name': name.strip()})
    return pd.DataFrame(data)

def replace_content(row):
    """
    Replaces the content with the section name if it is in the additional_strings list.
    """
    section_code = row['Section']
    section_name = df_legend.loc[df_legend['Section Code'] == section_code, 'Section Name'].values
    if section_name:
        row['Content'] = section_name[0]
    return row


def extract_info(row):
    """
    Extracts the section code and name from the section string.
    """
    if '\n' in row['Content']:
        section_name, content_part = row['Section'], row['Content'].split('\n', 1)[0]
        row['Nazwa Sekcji'] = section_name + ' ' + content_part
        row['Content'] = row['Content'].split('\n', 1)[1]
    else:
        row['Nazwa Sekcji'] = row['Section'] + ' ' + row['Content']
    return row

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
            if row['NAZWA_Sekcji'][5]=='.':
                first_three_letters = row['NAZWA_Sekcji'][:5]
            else:
                first_three_letters = row['NAZWA_Sekcji'][:3]
            matching_row = merged_df[merged_df['NAZWA_Sekcji'].str.startswith(first_three_letters)].iloc[0]
            merged_df.at[index, 'id sekcji nadrzędnej (Stała)'] = matching_row['ID SekcjI (stała)']

    merged_df['id sekcji nadrzędnej (Stała)'][0] = 1
    merged_df['ID_TAB'] = 1
    merged_df['data SFCR']=rok
    merged_df['wersja SFCR']=1
    merged_df['numer zakładu w systemie UKNF (kod zakładu)'] = kodLEI
    return merged_df

def create_section_df(text, sections, filename):
    """
    Creates a DataFrame from the text and sections.
    """
    document_text = text
    data = {'Section': [], 'Content': []}
    start_idx = 0
    for section in sections:
        start_marker = section
        end_marker = sections[sections.index(section) + 1] if sections.index(section) + 1 < len(sections) else None
        start_idx = document_text.find(start_marker, start_idx)
        end_idx = document_text.find(end_marker, start_idx) if end_marker else len(document_text)
        content = document_text[start_idx + len(start_marker):end_idx].strip()
        start_idx = end_idx
        data['Section'].append(section)
        data['Content'].append(content)
    df = pd.DataFrame(data)
    df = df.apply(replace_content, axis=1)
    df = df.apply(extract_info, axis=1)
    df.rename(columns={'Nazwa Sekcji': 'NAZWA_Sekcji','Content':'treść'},inplace=True)
    section_ids_path = "data/sekcje.csv"
    sections_ids_df= pd.read_csv(section_ids_path, sep=';')

    merged_df = pd.merge(df, sections_ids_df, left_on='NAZWA_Sekcji', right_on='Nazwa Sekcji (według Rozporządzenia)', how='left')
    merged_df.drop(columns=['Nazwa Sekcji (według Rozporządzenia)', 'Section'], inplace=True)


    rok, kodLEI, nazwa = extract_variables_from_filename(filename)

    merged_df = fulfill_df(merged_df, rok, kodLEI)
    return merged_df


df_legend = create_additional_df()

def main():
    filename = "2023_SFCR_259400IBCICD0KY7ZW46_TU ALLIANZ ŻYCIE POLSKA S.A..pdf"
    pdf_path = os.path.join("data", filename)
    text = extract_text_from_pdf(pdf_path)
    sections = find_unique_strings(text)
    sections = list(sections)
    sections.sort()
    merged_df = create_section_df(text, sections, filename)
    merged_df.to_csv('data/sections.csv', index=False, sep=';')
if __name__ == '__main__':
    main()