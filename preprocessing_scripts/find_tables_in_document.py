
import camelot
import pickle

def get_all_tables(path_to_pdf:str) -> list:
    """Extracts all tables from PDF file.

    Args:
        path_to_pdf (str): path to PDF file

    Returns:
        list: list of tables
    """
    tables = camelot.read_pdf(path_to_pdf, pages='all',strip_text='\n')
    return tables

def check_required_rows(tables:list, i:int, required_rows:list, present_rows:dict) -> (list,dict):
    """Checks if required rows are in table.

    Args:
        tables (list): list of tables
        i (int): index of first part of table
        required_rows (list): list of required rows
        present_rows (dict): dictionary with required rows and if they are in table

    Returns:
        list: list of parts of table
        dict: dictionary with required rows and if they are in table
    """
    table_parts = []
    table = tables[i].df
    table_parts.append(table)
    code_col = table.iloc[:,1]
    for row in required_rows:
        if sum(code_col == row) > 0:
            present_rows[row] = True
        else:
            if i != (len(tables)-1):
                table = tables[i+1].df
                code_col = table.iloc[:,1]
                if sum(code_col == row) >0:
                    present_rows[row] = True
                    table_parts.append(table)
                    i+=1
                else:
                    break
            else:
                break

    return table_parts, present_rows

def check_required_cols(tables:list, i:int, required_cols:int) -> bool:
    """Checks if required columns are in table.

    Args:
        tables (list): list of tables
        i (int): index of first part of table
        required_cols (int): number of required columns

    Returns:
        bool: True if table has required columns
    """
    table = tables[i].df
    if table.shape[1] == required_cols:
        return True
    else:
        return False
    
def find_first_part_of_table(tables:list, name:str, code:str) -> int:
    """Finds first part of table.

    Args:
        tables (list): list of tables
        name (str): content of first required row
        code (str): code of first required row

    Returns:
        int: index of first part of table
    """
    table_present = False
    i = 0
    for i in range(len(tables)):
        table = tables[i].df
        name_col = table.iloc[:,0]
        if sum(name_col == name) > 0:
            code_col = table.iloc[:,1]
            if sum(code_col == code) > 0:
                table_present = True
                break
        i+=1
    return i, table_present

def check_if_table_in_document(tables:list, table_name:str) -> (bool, list, dict,bool):
    """Checks if PDF file contains table.

    Args:
        tables (list): all tables from pdf
        table_name (str): name of table

    Returns:
        bool: True if table is in PDF file
        list: table
        dict: dictionary with required rows and if they are in table
        bool: True if table has required columns
    """
    required_rows_dict = {'S_02_01_02_01': ["R0030", "R0040", "R0050", "R0060", "R0070", "R0080", "R0090", "R0100", "R0110", "R0120", "R0130", "R0140", "R0150", "R0160", "R0170", "R0180", "R0190", "R0200", "R0210", "R0220", "R0230", "R0240", "R0250", "R0260", "R0270", "R0280", "R0290", "R0300", "R0310", "R0320", "R0330", "R0340", "R0350", "R0360", "R0370", "R0380", "R0390", "R0400", "R0410", "R0420", "R0500", "R0510", "R0520", "R0530", "R0540", "R0550", "R0560", "R0570", "R0580", "R0590", "R0600", "R0610", "R0620", "R0630", "R0640", "R0650", "R0660", "R0670", "R0680", "R0690", "R0700", "R0710", "R0720", "R0740", "R0750", "R0760", "R0770", "R0780", "R0790", "R0800", "R0810", "R0820", "R0830", "R0840", "R0850", "R0860", "R0870", "R0880", "R0900", "R1000"],
                          'S_05_01_02_01': ["R0110", "R0120", "R0130", "R0140", "R0200", "R0210", "R0220", "R0230", "R0240", "R0300", "R0310", "R0320", "R0330", "R0340", "R0400", "R0410", "R0420", "R0430", "R0440", "R0500", "R0550", "R1200", "R1300"],
                          'S_05_01_02_02': ["R1410", "R1420", "R1500", "R1510", "R1520", "R1600", "R1610", "R1620", "R1700", "R1710", "R1720", "R1800", "R1900", "R2500", "R2600"],
                          'S_05_02_01_01': ["R0110", "R0120", "R0130", "R0140", "R0200", "R0210", "R0220", "R0230", "R0240", "R0300", "R0310", "R0320", "R0330", "R0340", "R0400", "R0410", "R0420", "R0430", "R0440", "R0500", "R0550"],
                          'S_05_02_01_02': ["R0110", "R0120", "R0130", "R0140", "R0200", "R0210", "R0220", "R0230", "R0240", "R0300", "R0310", "R0320", "R0330", "R0340", "R0400", "R0410", "R0420", "R0430", "R0440", "R0500", "R0550"],
                          'S_05_02_01_03': ["R0110", "R0120", "R0130", "R0140", "R0200", "R0210", "R0220", "R0230", "R0240", "R0300", "R0310", "R0320", "R0330", "R0340", "R0400", "R0410", "R0420", "R0430", "R0440", "R0500", "R0550", "R1200", "R1300"],
                          'S_05_02_01_04': ["R1410", "R1420", "R1500", "R1510", "R1520", "R1600", "R1610", "R1620", "R1700", "R1710", "R1720", "R1800", "R1900"],
                          'S_05_02_01_05': ["R1410", "R1420", "R1500", "R1510", "R1520", "R1600", "R1610", "R1620", "R1700", "R1710", "R1720", "R1800", "R1900"],
                          'S_06_02_01_06': ["R1410", "R1420", "R1500", "R1510", "R1520", "R1600", "R1610", "R1620", "R1700", "R1710", "R1720", "R1800", "R1900", "R2500", "R2600"],
                          'S_12_01_02_01': ["R0010", "R0020", "R0030", "R0080", "R0090", "R0100", "R0110", "R0120", "R0130", "R0200"],
                          'S_17_01_02_01': ["R0010", "R0050", "R0060", "R0140", "R0150", "R0160", "R0240", "R0250", "R0260", "R0270", "R0280", "R0290", "R0300", "R0310", "R0320", "R0330", "R0340"],
                          'S_19_01_21_01': ["R0100", "R0101", "R0102", "R0103", "R0104", "R0105", "R0106", "R0107", "R0108", "R0109", "R0110"],
                          'S_19_01_21_02': ["R0100", "R0160", "R0170", "R0180", "R0190", "R0200", "R0210", "R0220", "R0230", "R0240", "R0250", "R0260"],
                          'S_19_01_21_03': ["R0100", "R0160", "R0170", "R0180", "R0190", "R0200", "R0210", "R0220", "R0230", "R0240", "R0250"],
                          'S_19_01_21_04': ["R0100", "R0160", "R0170", "R0180", "R0190", "R0200", "R0210", "R0220", "R0230", "R0240", "R0250", "R0260"],
                          'S_22_01_21_01': ["R0010", "R0020", "R0050", "R0090", "R0100", "R0110"],
                          'S_23_01_01_01': ["R0010", "R0030", "R0040", "R0050", "R0070", "R0090", "R0110", "R0130", "R0140", "R0160", "R0180", "R0220", "R0230", "R0290", "R0300", "R0310", "R0320", "R0330", "R0340", "R0350", "R0360", "R0370", "R0390", "R0400", "R0500", "R0510", "R0540", "R0550", "R0580", "R0600", "R0620", "R0640"],
                          'S_23_01_01_02': ["R0700", "R0710", "R0720", "R0730", "R0740", "R0760", "R0770", "R0780", "R0790"],
                          'S_25_01_21_01': ["R0010", "R0020", "R0030", "R0040", "R0050", "R0060", "R0070", "R0100"],
                          'S_25_01_21_02': ["R0130", "R0140", "R0150", "R0160", "R0200", "R0210", "R0220", "R0400", "R0410", "R0420", "R0430", "R0440"],
                          'S_25_01_21_03': ["R0030", "R0040", "R0050"],
                          'S_25_01_21_04': ['R0590'],
                          'S_25_01_21_05': ["R0640", "R0650", "R0660", "R0670", "R0680", "R0690"],
                          'S_25_02_21_01': [''],
                          'S_25_02_21_02': ["R0110", "R0060", "R0160", "R0200", "R0210", "R0220", "R0300", "R0310", "R0400", "R0410", "R0420", "R0430", "R0440"],
                          'S_25_02_21_03': ['R0590'],
                          'S_25_02_21_05': ["R0640", "R0650", "R0660", "R0670", "R0680", "R0690"],
                          'S_25_03_21_01': [''],
                          'S_25_03_21_02': ["R0110", "R0060", "R0160", "R0200", "R0210", "R0220", "R0300", "R0310", "R0410", "R0420", "R0430", "R0440"],
                          'S_25_03_21_03': ['R0590'],
                          'S_25_03_21_05': ["R0640", "R0650", "R0660", "R0670", "R0680", "R0690"],
                          'S_28_01_01_02': ["R0020", "R0030", "R0040", "R0050", "R0060", "R0070", "R0080", "R0090", "R0100", "R0110", "R0120", "R0130", "R0140", "R0150", "R0160", "R0170"],
                          'S_28_01_01_03': ['R0200'],
                          'S_28_01_01_04': ['R0210','R0220','R0230','R0240','R0250'],
                          'S_28_01_01_05': ['R0300','R0310','R0320','R0330','R0340','R0350','R0400'],
                          'S_28_02_01_01': ['R0010'],
                          'S_28_01_01_01': ['R0010'],
                          'S_28_02_01_02': ["R0020", "R0030", "R0040", "R0050", "R0060", "R0070", "R0080", "R0090", "R0100", "R0110", "R0120", "R0130", "R0140", "R0150", "R0160", "R0170"],
                          'S_28_02_01_03': ['R0200'],
                          'S_28_02_01_04': ['R0210','R0220','R0230','R0240','R0250'],
                          'S_28_02_01_05': ['R0300','R0310','R0320','R0330','R0340','R0350','R0400'],
                          'S_28_02_01_06': ['R0500','R0510','R0520','R0530','R0540','R0550','R0560']

                     }
    required_cols_dict = {'S_02_01_02_01': 3,
                          'S_05_01_02_01': 19,
                          'S_05_01_02_02': 11,
                          'S_05_02_01_01': 3,
                          'S_05_02_01_02': 3,
                          'S_05_02_01_03': 3,
                          'S_05_02_01_04': 3,
                          'S_05_02_01_05': 3,
                          'S_06_02_01_06': 3,
                          'S_12_01_02_01': 18,
                          'S_17_01_02_01': 19,
                          'S_19_01_21_01': 13,
                          'S_19_01_21_02': 4,
                          'S_19_01_21_03': 13,
                          'S_19_01_21_04': 3,
                          'S_22_01_21_01': 7,
                          'S_23_01_01_01': 7,
                          'S_23_01_01_02': 3,
                          'S_25_01_21_01': 4,
                          'S_25_01_21_02': 3,
                          'S_25_01_21_03': 3,
                          'S_25_01_21_04': 3,
                          'S_25_01_21_05': 3,
                          'S_25_02_21_01': 2,
                          'S_25_02_21_02': 3,
                          'S_25_02_21_03': 3,
                          'S_25_02_21_05': 3,
                          'S_25_03_21_01': 3,
                          'S_25_03_21_02': 3,
                          'S_25_03_21_03': 3,
                          'S_25_03_21_05': 3,
                          'S_28_01_01_02': 4,
                          'S_28_01_01_03': 3,
                          'S_28_01_01_04': 4,
                          'S_28_01_01_05': 3,
                          'S_28_02_01_01': 4,
                          'S_28_01_01_01': 3,
                          'S_28_02_01_02': 6,
                          'S_28_02_01_03': 4,
                          'S_28_02_01_04': 6,
                          'S_28_02_01_05': 3,
                          'S_28_02_01_06': 4}
    name_dict = {'S_02_01_02_01': 'Wartości niematerialne i prawne',
                 'S_05_01_02_01': 'Brutto - Bezpośrednia działalność ubezpieczeniowa',
                 'S_05_01_02_02': 'Brutto',
                 'S_05_02_01_01': 'Brutto - Bezpośrednia działalność ubezpieczeniowa',
                 'S_05_02_01_02': 'Brutto - Bezpośrednia działalność ubezpieczeniowa',
                 'S_05_02_01_03': 'Brutto - Bezpośrednia działalność ubezpieczeniowa',
                 'S_05_02_01_04': 'Brutto',
                 'S_05_02_01_05': 'Brutto',
                 'S_06_02_01_06': 'Brutto',
                 'S_12_01_02_01': 'Rezerwy techniczno-ubezpieczeniowe obliczane łącznie',
                 'S_17_01_02_01': 'Rezerwy techniczno-ubezpieczeniowe obliczane łącznie',
                 'S_19_01_21_01': 'Wcześniejsze lata',
                 'S_19_01_21_02': 'Wcześniejsze lata',
                 'S_19_01_21_03': 'Wcześniejsze lata',
                 'S_19_01_21_04': 'Wcześniejsze lata',
                 'S_22_01_21_01': 'Rezerwy techniczno-ubezpieczeniowe',
                 'S_23_01_01_01': 'Kapitał zakładowy (wraz z akcjami własnymi)',
                 'S_23_01_01_02': 'Nadwyżka aktywów nad zobowiązaniami',
                 'S_25_01_21_01': 'Ryzyko rynkowe',
                 'S_25_01_21_02': 'Ryzyko operacyjne',
                 'S_25_01_21_03': 'Ryzyko ubezpieczeniowe w ubezpieczeniach na życie',
                 'S_25_01_21_04': 'Podejście oparte na średniej stawce podatkowej',
                 'S_25_01_21_05': 'LAC DT',
                 'S_25_02_21_01': 'Niepowtarzalny numer składnika',
                 'S_25_02_21_02': 'Niezdywersyfikowane składniki ogółem',
                 'S_25_02_21_03': 'Podejście oparte na średniej stawce podatkowej',
                 'S_25_02_21_05': 'Kwota/wartość szacunkowa LAC DT',
                 'S_25_03_21_01': 'Niepowtarzalny numer składnika',
                 'S_25_03_21_02': 'Niezdywersyfikowane składniki ogółem',
                 'S_25_03_21_03': 'Podejście oparte na średniej stawce podatkowej',
                 'S_25_03_21_05': 'Kwota/wartość szacunkowa LAC DT',
                 'S_28_01_01_02': 'Ubezpieczenia pokrycia kosztów świadczeń medycznych i reasekuracja proporcjonalna',
                 'S_28_01_01_03': 'MCRL Wynik',
                 'S_28_01_01_04': 'Zobowiązania z tytułu ubezpieczeń z udziałem w zyskach - świadczenia gwarantowane',
                 'S_28_01_01_05': 'Liniowy MCR',
                 'S_28_02_01_01': 'Komponent formuły liniowej dla zobowiązań ubezpieczeniowych i reasekuracyjnych z tytułu ubezpieczeń innych niż ubezpieczenia na życie',
                 'S_28_01_01_01': 'MCRNL Wynik',
                 'S_28_02_01_02': 'Ubezpieczenia pokrycia kosztów świadczeń medycznych i reasekuracja proporcjonalna',
                 'S_28_02_01_03': 'Komponent formuły liniowej dla zobowiązań ubezpieczeniowych i reasekuracyjnych z tytułu ubezpieczeń na życie',
                 'S_28_02_01_04': 'Zobowiązania z tytułu ubezpieczeń z udziałem w zyskach - świadczenia gwarantowane',
                 'S_28_02_01_05': 'Liniowy MCR',
                 'S_28_02_01_06': 'Liniowy hipotetyczny MCR'
                 }
    
    required_rows = required_rows_dict[table_name]
    required_cols = required_cols_dict[table_name]
    name = name_dict[table_name]

    present_rows = {key: False for key in required_rows}

    i,table_present = find_first_part_of_table(tables,name,required_rows[0])
    
    if not table_present:
        return table_present, [], present_rows, False
    table_parts, present_rows = check_required_rows(tables, i, required_rows, present_rows)
    all_cols_present = check_required_cols(tables,i,required_cols)

    return True, table_parts, present_rows, all_cols_present


def main():
    # tables = get_all_tables('C:\\Users\\ltoma\\OneDrive\\Dokumenty\\Python\\Supervision-hack-3\\data\\SFCR NN TUNZ 2021.pdf')
    # with open('list_nn.pkl', 'wb') as f:
    #     pickle.dump(tables, f)


    with open('list_nn.pkl', 'rb') as f:
        list = pickle.load(f)
    table_present, table_parts, present_rows, all_cols_present = check_if_table_in_document(list,'S_25_01_21_01')
    print(table_present)
    print(present_rows)
    print(table_parts)
    print(all_cols_present)
    

if __name__ == '__main__':
    main()


