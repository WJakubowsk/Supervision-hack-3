import pandas as pd

def check_if_keywords_in_section(sections:pd.DataFrame, section:int, key_words:list) -> bool:
    """
    Checks if key words are in the section.

    Args:
        sections (DataFrame): dataframe containing sections
        section (int): section id
        key_words (list): list of key words

    Returns:
        bool: True if key words are in the section, False otherwise
    """
    section = sections.loc[(sections['ID SekcjI (stała)']==section) | (sections['id sekcji nadrzędnej (Stała)']==section),:]
    section = section['treść'].str.cat(sep=' ')
    
    for key_word in key_words:
        if key_word in section:
            return True
    return False

def check_completness(sections:pd.DataFrame) -> pd.DataFrame:
    """
    Checks the completness of the document.

    Args:
        sections (DataFrame): dataframe containing sections

    Returns:
        pd.DataFrame: dataframe containing the completness of the document
    """
    completness = pd.DataFrame(columns=['id_pytania','kompletnosc','id_sekcji'])


    question_1 = check_if_keywords_in_section(sections, 3, ['nazwa i forma prawna', 'Towarzystwo', 'Zakład', 'TU', 'ZU', 'TUiR', 'ZUiR', 'TUnŻ', 'TUnŻiR', 'TUW'])   
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':1,'kompletnosc':question_1,'id_sekcji':3},index=[0])], ignore_index=True)

    question_2 = check_if_keywords_in_section(sections,3,['organ nadzoru', 'nadzór nad grupą'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':2,'kompletnosc':question_2,'id_sekcji':3},index=[0])], ignore_index=True)

    question_3 = check_if_keywords_in_section(sections,3,['biegły rewident','audytor','audyt'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':3,'kompletnosc':question_3,'id_sekcji':3},index=[0])], ignore_index=True)

    question_4 = check_if_keywords_in_section(sections,3,['udziałowiec'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':4,'kompletnosc':question_4,'id_sekcji':3},index=[0])], ignore_index=True)

    question_5 = check_if_keywords_in_section(sections,3,['pośredni','bezpośredni','udziałowiec'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':5,'kompletnosc':question_5,'id_sekcji':3},index=[0])], ignore_index=True)

    question_6 = check_if_keywords_in_section(sections,3,['struktura','pozycja','miejsce'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':6,'kompletnosc':question_6,'id_sekcji':3},index=[0])], ignore_index=True)

    question_7 = check_if_keywords_in_section(sections,3,['jednoski powiązane','udziały','kraj'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':7,'kompletnosc':question_7,'id_sekcji':3},index=[0])], ignore_index=True)

    question_8 = check_if_keywords_in_section(sections,3,['struktura','uproszczona'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':8,'kompletnosc':question_8,'id_sekcji':3},index=[0])], ignore_index=True)

    question_9 = check_if_keywords_in_section(sections,3,['linie biznesowe','obszar','geograficzne'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':9,'kompletnosc':question_9,'id_sekcji':3},index=[0])], ignore_index=True)

    question_10 = check_if_keywords_in_section(sections,3,['zdarzenia','gospodarcze'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':10,'kompletnosc':question_10,'id_sekcji':3},index=[0])], ignore_index=True)

    question_11 = check_if_keywords_in_section(sections,4,['wyniki z działalności','w podziale na','linie biznesowe','geograficzne','składka','odszkodowania','koszty'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':11,'kompletnosc':question_11,'id_sekcji':4},index=[0])], ignore_index=True)

    question_12 = check_if_keywords_in_section(sections,5,['działalność lokacyjna','działalność inwestycyjna','wynik','przychody','koszty','lokaty','typy aktywów'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':12,'kompletnosc':question_12,'id_sekcji':5},index=[0])], ignore_index=True)

    question_13 = check_if_keywords_in_section(sections,5,['zyski','straty','kapitał'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':13,'kompletnosc':question_13,'id_sekcji':5},index=[0])], ignore_index=True)

    question_14 = check_if_keywords_in_section(sections,5,['sekurytyzacja'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':14,'kompletnosc':question_14,'id_sekcji':5},index=[0])], ignore_index=True)

    question_15 = check_if_keywords_in_section(sections,6,['pozostałe przychody','pozostałe rodzaje','koszty'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':15,'kompletnosc':question_15,'id_sekcji':6},index=[0])], ignore_index=True)

    question_16 = check_if_keywords_in_section(sections,6,['leasing'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':16,'kompletnosc':question_16,'id_sekcji':6},index=[0])], ignore_index=True)

    question_17 = check_if_keywords_in_section(sections,7,['inne informacje'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':17,'kompletnosc':question_17,'id_sekcji':7},index=[0])], ignore_index=True)

    question_18 = check_if_keywords_in_section(sections,9,['struktura', 'skład', 'zarząd', 'komitety', 'zakres', 'kompetencja', 'odpowiedzialność', 'obowiązek', 'odpowiedzialny'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':18,'kompletnosc':question_18,'id_sekcji':9},index=[0])], ignore_index=True)

    question_19 = check_if_keywords_in_section(sections,9,['struktura', 'rada nadzorcza', 'komitety', 'kompetencja', 'zakres', 'odpowiedzialność', 'obowiązek'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':19,'kompletnosc':question_19,'id_sekcji':9},index=[0])], ignore_index=True)

    question_20 = check_if_keywords_in_section(sections,9,['funkcja kluczowa','obowiązek','zadania'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':20,'kompletnosc':question_20,'id_sekcji':9},index=[0])], ignore_index=True)

    question_21 = check_if_keywords_in_section(sections,9,['zmiana','system zarządzania'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':21,'kompletnosc':question_21,'id_sekcji':9},index=[0])], ignore_index=True)

    question_22 = check_if_keywords_in_section(sections,9,['wynagrodzenia','zasada','polityka','stałe','zmienne','składniki'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':22,'kompletnosc':question_22,'id_sekcji':9},index=[0])], ignore_index=True)

    question_23 = check_if_keywords_in_section(sections,9,['uprawnienia do akcji','opcje na akcje','zmienne','składniki','wynagrodzenia'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':23,'kompletnosc':question_23,'id_sekcji':9},index=[0])], ignore_index=True)

    question_24 = check_if_keywords_in_section(sections,9,['programy emerytalno-rentowe','wcześniejsze emerytury'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':24,'kompletnosc':question_24,'id_sekcji':9},index=[0])], ignore_index=True)

    question_25 = check_if_keywords_in_section(sections,9,['istotne transakcje'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':25,'kompletnosc':question_25,'id_sekcji':9},index=[0])], ignore_index=True)

    question_26 = check_if_keywords_in_section(sections,9,['funkcje kluczowe','uprawnienia','zasoby','niezależność','raportować'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':26,'kompletnosc':question_26,'id_sekcji':9},index=[0])], ignore_index=True)

    question_27 = check_if_keywords_in_section(sections,9,['adekwatność systemu zarządzania','ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':27,'kompletnosc':question_27,'id_sekcji':9},index=[0])], ignore_index=True)

    question_28 = check_if_keywords_in_section(sections,10,['umiejętności','kwalifikacje','wiedza'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':28,'kompletnosc':question_28,'id_sekcji':10},index=[0])], ignore_index=True)

    question_29 = check_if_keywords_in_section(sections,10,['kompetencja','reputacja','procedura','ocena'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':29,'kompletnosc':question_29,'id_sekcji':10},index=[0])], ignore_index=True)

    question_30 = check_if_keywords_in_section(sections,11,['zarządzanie ryzykiem', 'strategia', 'proces', 'procedura','pomiar','monitorowanie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':30,'kompletnosc':question_30,'id_sekcji':11},index=[0])], ignore_index=True)

    question_31 = check_if_keywords_in_section(sections,11,['system zarządzania ryzykiem', 'funkcja zarządzania ryzykiem', 'struktura', 'decyzje'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':31,'kompletnosc':question_31,'id_sekcji':11},index=[0])], ignore_index=True)

    question_32 = check_if_keywords_in_section(sections,11,['ORSA', 'Własna Ocena Ryzyka i Wypłacalności', 'proces'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':32,'kompletnosc':question_32,'id_sekcji':11},index=[0])], ignore_index=True)

    question_33 = check_if_keywords_in_section(sections,11,['przegląd','zatwierdzanie','co najmniej'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':33,'kompletnosc':question_33,'id_sekcji':11},index=[0])], ignore_index=True)

    question_34 = check_if_keywords_in_section(sections,11,['potrzeby w zakresie wypłacalności', 'profil ryzyka', 'zarządzanie kapitałem','apetyt'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':34,'kompletnosc':question_34,'id_sekcji':11},index=[0])], ignore_index=True)

    question_35 = check_if_keywords_in_section(sections,11,['model wewnętrzny', 'zarządzanie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':35,'kompletnosc':question_35,'id_sekcji':11},index=[0])], ignore_index=True)

    question_36 = check_if_keywords_in_section(sections,11,['model wewnętrzny', 'zarząd', 'rada nadzorcza'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':36,'kompletnosc':question_36,'id_sekcji':11},index=[0])], ignore_index=True)

    question_37 = check_if_keywords_in_section(sections,11,['model wewnętrzny', 'zmiana', 'zarządzanie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':37,'kompletnosc':question_37,'id_sekcji':11},index=[0])], ignore_index=True)

    question_38 = check_if_keywords_in_section(sections,11,['model wewnętrzny', 'walidacja'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':38,'kompletnosc':question_38,'id_sekcji':11},index=[0])], ignore_index=True)

    question_39 = check_if_keywords_in_section(sections,12,['system kontroli wewnętrznej'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':39,'kompletnosc':question_39,'id_sekcji':12},index=[0])], ignore_index=True)

    question_40 = check_if_keywords_in_section(sections,12,['funkcja zgodności z przepisami'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':40,'kompletnosc':question_40,'id_sekcji':12},index=[0])], ignore_index=True)

    question_41 = check_if_keywords_in_section(sections,13,['funkcja audytu wewnętrznego'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':41,'kompletnosc':question_41,'id_sekcji':13},index=[0])], ignore_index=True)

    question_42 = check_if_keywords_in_section(sections,13,['niezależność', 'obiektywność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':42,'kompletnosc':question_42,'id_sekcji':13},index=[0])], ignore_index=True)

    question_43 = check_if_keywords_in_section(sections,14,['funkcja aktuarialna'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':43,'kompletnosc':question_43,'id_sekcji':14},index=[0])], ignore_index=True)

    question_44 = check_if_keywords_in_section(sections,15,['outsourcing', 'zasada'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':44,'kompletnosc':question_44,'id_sekcji':15},index=[0])], ignore_index=True)

    question_45 = check_if_keywords_in_section(sections,15,['czynności','podstawowe','ważne','outsourcing'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':45,'kompletnosc':question_45,'id_sekcji':15},index=[0])], ignore_index=True)

    question_46 = check_if_keywords_in_section(sections,15,['jurysdykcja'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':46,'kompletnosc':question_46,'id_sekcji':15},index=[0])], ignore_index=True)

    question_47 = check_if_keywords_in_section(sections,16,['inne informacje'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':47,'kompletnosc':question_47,'id_sekcji':16},index=[0])], ignore_index=True)

    question_48 = check_if_keywords_in_section(sections,18,['aktuarialne', 'ubezpieczeniowe', 'ekspozycja', 'pozabilansowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':48,'kompletnosc':question_48,'id_sekcji':18},index=[0])], ignore_index=True)

    question_49 = check_if_keywords_in_section(sections,18,['ocena ryzyka', 'pomiar', 'zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':49,'kompletnosc':question_49,'id_sekcji':18},index=[0])], ignore_index=True)

    question_50 = check_if_keywords_in_section(sections,18,['istotne ryzyka','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':50,'kompletnosc':question_50,'id_sekcji':18},index=[0])], ignore_index=True)

    question_51 = check_if_keywords_in_section(sections,18,['koncentracja ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':51,'kompletnosc':question_51,'id_sekcji':18},index=[0])], ignore_index=True)

    question_52 = check_if_keywords_in_section(sections,18,['technika ograniczania ryzyka', 'monitorowanie','skuteczność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':52,'kompletnosc':question_52,'id_sekcji':18},index=[0])], ignore_index=True)

    question_53 = check_if_keywords_in_section(sections,18,['testy warunków skrajnych', 'analiza warunków skrajnych', 'analiza wrażliwości'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':53,'kompletnosc':question_53,'id_sekcji':18},index=[0])], ignore_index=True)

    question_54 = check_if_keywords_in_section(sections,18,['spólka celowa'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':54,'kompletnosc':question_54,'id_sekcji':18},index=[0])], ignore_index=True)

    question_55 = check_if_keywords_in_section(sections,19,['rynkowe','ekspozycja','pozabilansowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':55,'kompletnosc':question_55,'id_sekcji':19},index=[0])], ignore_index=True)

    question_56 = check_if_keywords_in_section(sections,19,['ocena ryzyka','pomiar','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':56,'kompletnosc':question_56,'id_sekcji':19},index=[0])], ignore_index=True)

    question_57 = check_if_keywords_in_section(sections,19,['istotne ryzyka','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':57,'kompletnosc':question_57,'id_sekcji':19},index=[0])], ignore_index=True)

    question_58 = check_if_keywords_in_section(sections,19,['ostrożnego inwestora','zasada'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':58,'kompletnosc':question_58,'id_sekcji':19},index=[0])], ignore_index=True)

    question_59 = check_if_keywords_in_section(sections,19,['koncentracja ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':59,'kompletnosc':question_59,'id_sekcji':19},index=[0])], ignore_index=True)

    question_60 = check_if_keywords_in_section(sections,19,['technika ograniczania ryzyka','monitorowanie','skuteczność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':60,'kompletnosc':question_60,'id_sekcji':19},index=[0])], ignore_index=True)

    question_61 = check_if_keywords_in_section(sections,19,['testy warunków skrajnych','analiza warunków skrajnych','analiza wrażliwości'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':61,'kompletnosc':question_61,'id_sekcji':19},index=[0])], ignore_index=True)

    question_62 = check_if_keywords_in_section(sections,20,['kredytowe','ekspozycja','pozabilansowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':62,'kompletnosc':question_62,'id_sekcji':20},index=[0])], ignore_index=True)

    question_63 = check_if_keywords_in_section(sections,20,['ocena ryzyka','pomiar','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':63,'kompletnosc':question_63,'id_sekcji':20},index=[0])], ignore_index=True)

    question_64 = check_if_keywords_in_section(sections,20,['istotne ryzyka','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':64,'kompletnosc':question_64,'id_sekcji':20},index=[0])], ignore_index=True)

    question_65 = check_if_keywords_in_section(sections,20,['ostrożnego inwestora','zasada'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':65,'kompletnosc':question_65,'id_sekcji':20},index=[0])], ignore_index=True)

    question_66 = check_if_keywords_in_section(sections,20,['koncentracja ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':66,'kompletnosc':question_66,'id_sekcji':20},index=[0])], ignore_index=True)

    question_67 = check_if_keywords_in_section(sections,20,['technika ograniczania ryzyka','monitorowanie','skuteczność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':67,'kompletnosc':question_67,'id_sekcji':20},index=[0])], ignore_index=True)

    question_68 = check_if_keywords_in_section(sections,20,['testy warunków skrajnych','analiza warunków skrajnych','analiza wrażliwości'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':68,'kompletnosc':question_68,'id_sekcji':20},index=[0])], ignore_index=True)

    question_69 = check_if_keywords_in_section(sections,21,['ryzyko płynności','ekspozycja','pozabilansowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':69,'kompletnosc':question_69,'id_sekcji':21},index=[0])], ignore_index=True)

    question_70 = check_if_keywords_in_section(sections,21,['ocena ryzyka','pomiar','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':70,'kompletnosc':question_70,'id_sekcji':21},index=[0])], ignore_index=True)

    question_71 = check_if_keywords_in_section(sections,21,['istotne ryzyka','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':71,'kompletnosc':question_71,'id_sekcji':21},index=[0])], ignore_index=True)

    question_72 = check_if_keywords_in_section(sections,21,['ostrożnego inwestora','zasada'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':72,'kompletnosc':question_72,'id_sekcji':21},index=[0])], ignore_index=True)

    question_73 = check_if_keywords_in_section(sections,21,['koncentracja ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':73,'kompletnosc':question_73,'id_sekcji':21},index=[0])], ignore_index=True)

    question_74 = check_if_keywords_in_section(sections,21,['techniki ograniczania ryzyka','monitorowanie','skuteczność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':74,'kompletnosc':question_74,'id_sekcji':21},index=[0])], ignore_index=True)

    question_75 = check_if_keywords_in_section(sections,21,['zyski z przyszłych składek'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':75,'kompletnosc':question_75,'id_sekcji':21},index=[0])], ignore_index=True)

    question_76 = check_if_keywords_in_section(sections,21,['testy warunków skrajnych','analiza warunków skrajnych','analiza wrażliwości'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':76,'kompletnosc':question_76,'id_sekcji':21},index=[0])], ignore_index=True)

    question_77 = check_if_keywords_in_section(sections,22,['operacyjne','ekspozycja','pozabilansowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':77,'kompletnosc':question_77,'id_sekcji':22},index=[0])], ignore_index=True)

    question_78 = check_if_keywords_in_section(sections,22,['ocena ryzyka','pomiar','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':78,'kompletnosc':question_78,'id_sekcji':22},index=[0])], ignore_index=True)

    question_79 = check_if_keywords_in_section(sections,22,['istotne ryzyka','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':79,'kompletnosc':question_79,'id_sekcji':22},index=[0])], ignore_index=True)

    question_80 = check_if_keywords_in_section(sections,22,['koncentracja ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':80,'kompletnosc':question_80,'id_sekcji':22},index=[0])], ignore_index=True)

    question_81 = check_if_keywords_in_section(sections,22,['technika ograniczania ryzyka','monitorowanie','skuteczność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':81,'kompletnosc':question_81,'id_sekcji':22},index=[0])], ignore_index=True)

    question_82 = check_if_keywords_in_section(sections,22,['testy warunków skrajnych','analiza warunków skrajnych','analiza wrażliwości'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':82,'kompletnosc':question_82,'id_sekcji':22},index=[0])], ignore_index=True)

    question_83 = check_if_keywords_in_section(sections,23,['pozostałe','ekspozycja','pozabilansowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':83,'kompletnosc':question_83,'id_sekcji':23},index=[0])], ignore_index=True)

    question_84 = check_if_keywords_in_section(sections,23,['ocena ryzyka','pomiar','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':84,'kompletnosc':question_84,'id_sekcji':23},index=[0])], ignore_index=True)

    question_85 = check_if_keywords_in_section(sections,23,['istotne ryzyka','zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':85,'kompletnosc':question_85,'id_sekcji':23},index=[0])], ignore_index=True)

    question_86 = check_if_keywords_in_section(sections,23,['koncentracja ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':86,'kompletnosc':question_86,'id_sekcji':23},index=[0])], ignore_index=True)

    question_87 = check_if_keywords_in_section(sections,23,['technika ograniczania ryzyka','monitorowanie','skuteczność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':87,'kompletnosc':question_87,'id_sekcji':23},index=[0])], ignore_index=True)

    question_88 = check_if_keywords_in_section(sections,23,['testy warunków skrajnych','analiza warunków skrajnych','analiza wrażliwości'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':88,'kompletnosc':question_88,'id_sekcji':23},index=[0])], ignore_index=True)

    question_89 = check_if_keywords_in_section(sections,24,['inne informacje'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':89,'kompletnosc':question_89,'id_sekcji':24},index=[0])], ignore_index=True)

    question_90 = check_if_keywords_in_section(sections,26,['aktywa','bilans','celów wypłacalności'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':90,'kompletnosc':question_90,'id_sekcji':26},index=[0])], ignore_index=True)

    question_91 = check_if_keywords_in_section(sections,26,['aktywa','metoda','podstawa','wycena','założenia','wartość'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':91,'kompletnosc':question_91,'id_sekcji':26},index=[0])], ignore_index=True)

    question_92 = check_if_keywords_in_section(sections,26,['metoda','wycena','ujmowanie','dane','ocena','szacunki'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':92,'kompletnosc':question_92,'id_sekcji':26},index=[0])], ignore_index=True)

    question_93 = check_if_keywords_in_section(sections,26,['różnica','wycena','podstawa','metoda','założenia'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':93,'kompletnosc':question_93,'id_sekcji':26},index=[0])], ignore_index=True)

    question_94 = check_if_keywords_in_section(sections,26,['wartości niematerialne i prawne','aktywny','rynek'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':94,'kompletnosc':question_94,'id_sekcji':26},index=[0])], ignore_index=True)

    question_95 = check_if_keywords_in_section(sections,26,['aktywa finansowe','model wyceny','rynek','aktywny','nieaktywny'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':95,'kompletnosc':question_95,'id_sekcji':26},index=[0])], ignore_index=True)

    question_96 = check_if_keywords_in_section(sections,26,['leasing','operacyjny','finansowy'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':96,'kompletnosc':question_96,'id_sekcji':26},index=[0])], ignore_index=True)

    question_97 = check_if_keywords_in_section(sections,26,['aktywa z tytułu odroczonego podatku dochodowego', 'tymczasowe różnice', 'straty podatkowe','ulgi podatkowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':97,'kompletnosc':question_97,'id_sekcji':26},index=[0])], ignore_index=True)

    question_98 = check_if_keywords_in_section(sections,26,['podmioty powiązane','metoda praw własności'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':98,'kompletnosc':question_98,'id_sekcji':26},index=[0])], ignore_index=True)

    question_99 = check_if_keywords_in_section(sections,26,['zmiana','zasady','wycena','ujmowanie','szacunki'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':99,'kompletnosc':question_99,'id_sekcji':26},index=[0])], ignore_index=True)

    question_100 = check_if_keywords_in_section(sections,26,['założenia','niepewność oszacowania'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':100,'kompletnosc':question_100,'id_sekcji':26},index=[0])], ignore_index=True)

    question_101 = check_if_keywords_in_section(sections,27,['rezerwy techniczno-ubezpieczeniowe','najlepsze oszacowania','margines ryzyka','linia biznesowa','opis','podstawy','metoda','założenia'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':101,'kompletnosc':question_101,'id_sekcji':27},index=[0])], ignore_index=True)

    question_102 = check_if_keywords_in_section(sections,27,['niepewność','wartość','rezerwy techniczno-ubezpieczeniowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':102,'kompletnosc':question_102,'id_sekcji':27},index=[0])], ignore_index=True)

    question_103 = check_if_keywords_in_section(sections,27,['linia biznesowa','różnica','wycena','podstawa','metoda','założenia'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':103,'kompletnosc':question_103,'id_sekcji':27},index=[0])], ignore_index=True)

    question_104 = check_if_keywords_in_section(sections,27,['korekta dopasowująca'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':104,'kompletnosc':question_104,'id_sekcji':27},index=[0])], ignore_index=True)

    question_105 = check_if_keywords_in_section(sections,27,['korekta z tytułu zmienności'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':105,'kompletnosc':question_105,'id_sekcji':27},index=[0])], ignore_index=True)

    question_106 = check_if_keywords_in_section(sections,27,['przejściowa struktura terminowej stopy procentowej wolnej od ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':106,'kompletnosc':question_106,'id_sekcji':27},index=[0])], ignore_index=True)

    question_107 = check_if_keywords_in_section(sections,27,['przejściowe odliczenie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':107,'kompletnosc':question_107,'id_sekcji':27},index=[0])], ignore_index=True)

    question_108 = check_if_keywords_in_section(sections,27,['kwoty należne z umów reasekuracji', 'spółki celowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':108,'kompletnosc':question_108,'id_sekcji':27},index=[0])], ignore_index=True)

    question_109 = check_if_keywords_in_section(sections,27,['zmiana','założenia'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':109,'kompletnosc':question_109,'id_sekcji':27},index=[0])], ignore_index=True)

    question_110 = check_if_keywords_in_section(sections,27,['uproszczenia','istotne','rezerwy techniczno-ubezpieczeniowe', 'margines ryzyka'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':110,'kompletnosc':question_110,'id_sekcji':27},index=[0])], ignore_index=True)

    question_111 = check_if_keywords_in_section(sections,28,['inne zobowiązania', 'pozostałe zobowiązania', 'pozostałe rezerwy','świadczenia emerytalne', 'zobowiązania finansowe inne niż'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':111,'kompletnosc':question_111,'id_sekcji':28},index=[0])], ignore_index=True)

    question_112 = check_if_keywords_in_section(sections,28,['wartość','wycena','metoda','założenia','podstaw'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':112,'kompletnosc':question_112,'id_sekcji':28},index=[0])], ignore_index=True)

    question_113 = check_if_keywords_in_section(sections,28,['dane wejściowe',' zasady','ujmowanie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':113,'kompletnosc':question_113,'id_sekcji':28},index=[0])], ignore_index=True)

    question_114 = check_if_keywords_in_section(sections,28,['różnica','wycena','podstawa','metoda','założenia'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':114,'kompletnosc':question_114,'id_sekcji':28},index=[0])], ignore_index=True)

    question_115 = check_if_keywords_in_section(sections,28,['leasing','finansowy','operacyjny'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':115,'kompletnosc':question_115,'id_sekcji':28},index=[0])], ignore_index=True)

    question_116 = check_if_keywords_in_section(sections,28,['zobowiązania', 'podatku dochodowego', 'kwota', 'tymczasowe różnice', 'nierozliczone', 'straty podatkowe', 'ulgi podatkowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':116,'kompletnosc':question_116,'id_sekcji':28},index=[0])], ignore_index=True)

    question_117 = check_if_keywords_in_section(sections,28,['charakter zobowiązań', 'oczekiwany czas przepływów', 'niepewność', 'korzyści', 'odchylenie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':117,'kompletnosc':question_117,'id_sekcji':28},index=[0])], ignore_index=True)

    question_118 = check_if_keywords_in_section(sections,28,['zobowiązania z tytułu świadczeń pracowniczych'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':118,'kompletnosc':question_118,'id_sekcji':28},index=[0])], ignore_index=True)

    question_119 = check_if_keywords_in_section(sections,28,['zmiana','ujmowanie','wycena','szacunek'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':119,'kompletnosc':question_119,'id_sekcji':28},index=[0])], ignore_index=True)

    question_120 = check_if_keywords_in_section(sections,28,['założenia','ocena','przyszłe','źródła','niepewność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':120,'kompletnosc':question_120,'id_sekcji':28},index=[0])], ignore_index=True)

    question_121 = check_if_keywords_in_section(sections,29,['alternatywne metody wyceny', 'aktywa', 'zobowiązania', 'założenia', 'niepewność', 'adekwatność', 'uzasadnienie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':121,'kompletnosc':question_121,'id_sekcji':29},index=[0])], ignore_index=True)

    question_122 = check_if_keywords_in_section(sections,30,['inne istotne informacje'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':122,'kompletnosc':question_122,'id_sekcji':30},index=[0])], ignore_index=True)

    question_123 = check_if_keywords_in_section(sections,32,['środki własne', 'cele', 'zasady', 'horyzont czasowy', 'zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':123,'kompletnosc':question_123,'id_sekcji':32},index=[0])], ignore_index=True)

    question_124 = check_if_keywords_in_section(sections,32,['środki własne', 'struktura','kategoria','jakość','zmiana','różnica'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':124,'kompletnosc':question_124,'id_sekcji':32},index=[0])], ignore_index=True)

    question_125 = check_if_keywords_in_section(sections,32,['pokrycie kapitałowego wymogu wypłacalności', 'kategorie', 'środki własne'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':125,'kompletnosc':question_125,'id_sekcji':32},index=[0])], ignore_index=True)

    question_126 = check_if_keywords_in_section(sections,32,['ograniczenia','wpływ','środki własne','kategoria'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':126,'kompletnosc':question_126,'id_sekcji':32},index=[0])], ignore_index=True)

    question_127 = check_if_keywords_in_section(sections,32,['pokrycie minimalnego wymogu kapitałowego', 'kategorie', 'środki własne'])    
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':127,'kompletnosc':question_127,'id_sekcji':32},index=[0])], ignore_index=True)

    question_128 = check_if_keywords_in_section(sections,32,['różnice','kapitał własny', 'nadwyżka aktywów nad zobowiązaniami'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':128,'kompletnosc':question_128,'id_sekcji':32},index=[0])], ignore_index=True)

    question_129 = check_if_keywords_in_section(sections,32,['przepisy przejściowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':129,'kompletnosc':question_129,'id_sekcji':32},index=[0])], ignore_index=True)

    question_130 = check_if_keywords_in_section(sections,32,['uzupełniające środki własne','metoda'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':130,'kompletnosc':question_130,'id_sekcji':32},index=[0])], ignore_index=True)

    question_131 = check_if_keywords_in_section(sections,32,['uzupełniające środki własne', 'opłacenie', 'data zatwierdzenia pozycji', 'czas'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':131,'kompletnosc':question_131,'id_sekcji':32},index=[0])], ignore_index=True)

    question_132 = check_if_keywords_in_section(sections,32,['uzupełniające środki własne', 'zmiana', 'wycena', 'dane wejściowe', 'doświadczenie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':132,'kompletnosc':question_132,'id_sekcji':32},index=[0])], ignore_index=True)

    question_133 = check_if_keywords_in_section(sections,32,['pozycje odliczone','dostępność'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':133,'kompletnosc':question_133,'id_sekcji':32},index=[0])], ignore_index=True)

    question_134 = check_if_keywords_in_section(sections,32,['dodatkowe współczynniki','dodatkowe wskaźniki'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':134,'kompletnosc':question_134,'id_sekcji':32},index=[0])], ignore_index=True)

    question_135 = check_if_keywords_in_section(sections,32,['podstawowe środki własne','uzupełniające środki własne'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':135,'kompletnosc':question_135,'id_sekcji':32},index=[0])], ignore_index=True)

    question_136 = check_if_keywords_in_section(sections,32,['dostępne','podporządkowane','jakość'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':136,'kompletnosc':question_136,'id_sekcji':32},index=[0])], ignore_index=True)

    question_137 = check_if_keywords_in_section(sections,32,['emisja','umorzone','środki własne'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':137,'kompletnosc':question_137,'id_sekcji':32},index=[0])], ignore_index=True)

    question_138 = check_if_keywords_in_section(sections,32,['podporządkowane','instrumenty dłużne'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':138,'kompletnosc':question_138,'id_sekcji':32},index=[0])], ignore_index=True)

    question_139 = check_if_keywords_in_section(sections,32,['mechanizm pokrywania strat','zdarzenie inicjujące'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':139,'kompletnosc':question_139,'id_sekcji':32},index=[0])], ignore_index=True)

    question_140 = check_if_keywords_in_section(sections,32,['elementy','rezerwa uzgodnieniowa','struktura'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':140,'kompletnosc':question_140,'id_sekcji':32},index=[0])], ignore_index=True)

    question_141 = check_if_keywords_in_section(sections,32,['przepisy przejściowe','kategorie'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':141,'kompletnosc':question_141,'id_sekcji':32},index=[0])], ignore_index=True)

    question_142 = check_if_keywords_in_section(sections,32,['przepisy przejściowe','data wezwania'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':142,'kompletnosc':question_142,'id_sekcji':32},index=[0])], ignore_index=True)

    question_143 = check_if_keywords_in_section(sections,32,['fundusz wyodrębniony',' korekta dopasowująca'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':143,'kompletnosc':question_143,'id_sekcji':32},index=[0])], ignore_index=True)

    question_144 = check_if_keywords_in_section(sections,32,['ograniczenia','odliczenia','obciążenia'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':144,'kompletnosc':question_144,'id_sekcji':32},index=[0])], ignore_index=True)

    question_145 = check_if_keywords_in_section(sections,33,['kapitałowy wymóg wypłacalności', 'SCR', 'Solvency Capital Requirement', 'minimalny wymóg kapitałowy', 'MCR', 'Minimum Capital Requirement'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':145,'kompletnosc':question_145,'id_sekcji':33},index=[0])], ignore_index=True)

    question_146 = check_if_keywords_in_section(sections,33,['moduł ryzyka', 'kategorie', 'składowe', 'moduły', 'podmoduły'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':146,'kompletnosc':question_146,'id_sekcji':33},index=[0])], ignore_index=True)

    question_147 = check_if_keywords_in_section(sections,33,['uproszczenia; moduły', 'podmoduły', 'formuła standardowa'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':147,'kompletnosc':question_147,'id_sekcji':33},index=[0])], ignore_index=True)

    question_148 = check_if_keywords_in_section(sections,33,['parametry specyficzne','parametry'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':148,'kompletnosc':question_148,'id_sekcji':33},index=[0])], ignore_index=True)

    question_149 = check_if_keywords_in_section(sections,33,['narzut kapitałowy', 'parametry specyficzne'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':149,'kompletnosc':question_149,'id_sekcji':33},index=[0])], ignore_index=True)

    question_150 = check_if_keywords_in_section(sections,33,['dane wejściowe'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':150,'kompletnosc':question_150,'id_sekcji':33},index=[0])], ignore_index=True)

    question_151 = check_if_keywords_in_section(sections,33,['zmiana'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':151,'kompletnosc':question_151,'id_sekcji':33},index=[0])], ignore_index=True)

    question_152 = check_if_keywords_in_section(sections,34,['nie dotyczy','nie korzysta'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':152,'kompletnosc':question_152,'id_sekcji':34},index=[0])], ignore_index=True)

    question_153 = check_if_keywords_in_section(sections,35,['cele','model wewnętrzny'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':153,'kompletnosc':question_153,'id_sekcji':35},index=[0])], ignore_index=True)

    question_154 = check_if_keywords_in_section(sections,35,['zakres','model wewnętrzny'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':154,'kompletnosc':question_154,'id_sekcji':35},index=[0])], ignore_index=True)

    question_155 = check_if_keywords_in_section(sections,35,['struktura','ryzyko','model wewnętrzny'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':155,'kompletnosc':question_155,'id_sekcji':35},index=[0])], ignore_index=True)

    question_156 = check_if_keywords_in_section(sections,35,['agregacja','efekt dywersyfikacji'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':156,'kompletnosc':question_156,'id_sekcji':35},index=[0])], ignore_index=True)

    question_157 = check_if_keywords_in_section(sections,35,['integracja częściowego modelu wewnętrznego z formułą standardową'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':157,'kompletnosc':question_157,'id_sekcji':35},index=[0])], ignore_index=True)

    question_158 = check_if_keywords_in_section(sections,35,['modele wykorzystywane'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':158,'kompletnosc':question_158,'id_sekcji':35},index=[0])], ignore_index=True)

    question_159 = check_if_keywords_in_section(sections,35,['różnica','metoda','założenia','formuła standardowa'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':159,'kompletnosc':question_159,'id_sekcji':35},index=[0])], ignore_index=True)

    question_160 = check_if_keywords_in_section(sections,35,['ryzyko niobjęte standardową formułą'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':160,'kompletnosc':question_160,'id_sekcji':35},index=[0])], ignore_index=True)

    question_161 = check_if_keywords_in_section(sections,35,['miara ryzyka','okres wykorzystywany w modelu wewnętrznym'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':161,'kompletnosc':question_161,'id_sekcji':35},index=[0])], ignore_index=True)

    question_162 = check_if_keywords_in_section(sections,35,['dane wykorzystywane w modelu wewnętrznym'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':162,'kompletnosc':question_162,'id_sekcji':35},index=[0])], ignore_index=True)

    question_163 = check_if_keywords_in_section(sections,36,['niezgodności z minimalnym wymogiem kapitałowym','okres','kwota','środki naprawcze'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':163,'kompletnosc':question_163,'id_sekcji':36},index=[0])], ignore_index=True)

    question_164 = check_if_keywords_in_section(sections,36,['niezgodność','kwota'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':164,'kompletnosc':question_164,'id_sekcji':36},index=[0])], ignore_index=True)

    question_165 = check_if_keywords_in_section(sections,36,['niezgodności z kapitałowym wymogiem wypłacalności','okres','kwota','środki naprawcze'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':165,'kompletnosc':question_165,'id_sekcji':36},index=[0])], ignore_index=True)

    question_166 = check_if_keywords_in_section(sections,36,['niezgodność','kwota'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':166,'kompletnosc':question_166,'id_sekcji':36},index=[0])], ignore_index=True)

    question_167 = check_if_keywords_in_section(sections,37,['inne istotne informacje'])
    completness = pd.concat([completness, pd.DataFrame({'id_pytania':167,'kompletnosc':question_167,'id_sekcji':37},index=[0])], ignore_index=True)


    return completness


def main():
    path = './dane_jakosciowe.csv' ### provide the name of the preprocesssed CSV with separated section of SFCR file
    df = pd.read_csv(path, index_col=0)
    completness = check_completness(df)
    print(completness)

if __name__ == "__main__":
    main()