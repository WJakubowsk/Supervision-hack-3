# Supervision Hack #3 

## Opis zadania
W zadaniu #SF_CRacker skupiliśmy się na stworzeniu narzędzia automatyzującego analizę plików SFCR. Ma ono ułatwić pracę urzytkownikom na codzień zajmującym się sprawozdaniami dotyczącymi wypłacalności i kondycji finansowej.

## Opis rozwiązania
Projekt składa się z wielu modułów, które razem tworzą docelowe narzędzie. Można wśród nich wyróżnić:
- algorytmy przeprowadzające web scraping
- kod dzielący nieustrukturyzowane pliki `.pdf` na podsekcje ułatwiające analizę któtszych fragmentów tekstu oraz eksportujący tabele do plików `.csv`
- weryfikacja kompletności plików SFCR poprzez weryfikację występowania słów kluczowych
- kod umożliwiający ekstrakcję tabel z plików
- aplikacja umożliwiająca użytkownikowi analizę oraz porównywanie zawartości plików dla różnych lat

### Struktura projektu
Główne komponenty aplikacji znajdują się w folderze `app`. Można w nim znaleźć skrypty aplikacji oraz foldery `preprocessing_scripts` oraz `scraper`, które odpowiednio zawierają algorytmy przetwarzające dane pozyskane z pdfów oraz te przeprowadzające web scraping.

Autorzy:
- Hubert Bujakowski
- Wiktor Jakubowski
- Jan Kruszewski
- Łukasz Tomaszewski
