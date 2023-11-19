from PyPDF2 import PdfReader
import nltk
import textstat
import string
nltk.download('punkt')
nltk.download('pl196x')

def extract_polish_sentences(text:str)->list[str]:
    """
    Extracts sentences from a text in Polish.
    :param text: text to extract sentences from
    :return: list of sentences
    """

    sentences = nltk.sent_tokenize(text, language='polish')
    return sentences

def average_number_of_words(sentences:list[str])->float:
    """
    Calculates the average number of words in a sentence.
    :param sentences: list of sentences
    :return: average number of words in a sentence
    """

    number_of_words = 0
    for sentence in sentences:
        number_of_words += len(sentence.split())
    return number_of_words / len(sentences)

def average_number_of_characters(sentences:list[str])->float:
    """
    Calculates the average number of characters in a sentence.
    :param sentences: list of sentences
    :return: average number of characters in a sentence
    """

    number_of_characters = 0
    for sentence in sentences:
        number_of_characters += len(sentence)
    return number_of_characters / len(sentences)

def average_number_of_syllables(sentences:list[str])->float:
    """
    Calculates the average number of syllables in a sentence.
    :param sentences: list of sentences
    :return: average number of syllables in a sentence
    """

    number_of_syllables = 0
    for sentence in sentences:
        number_of_syllables += textstat.syllable_count(sentence, lang='pl_PL')
    return number_of_syllables / len(sentences)

def count_punctuation(text:str) -> dict[str, int]:
    """
    Counts the number of punctuation marks in a text.
    :param text: text to count punctuation marks in
    :return: number of punctuation marks
    """
    punctation_count = {'.':text.count('.'),
                        ',':text.count(','),
                        ';':text.count(';'),
                        ':':text.count(':'),
                        '!':text.count('!'),
                        '?':text.count('?'),
                        '-':text.count('-')
                        }
    return punctation_count

def main():
    reader = PdfReader("C:\\Users\\ltoma\\Desktop\\2022-SFCR-TUIR-Sprawozdanie-o-wyplacalnosci-i-kondycji-finansowej.pdf")

    full_text = ''
    for page in reader.pages:
        full_text += page.extract_text()

    sentences = extract_polish_sentences(full_text)
    print(average_number_of_words(sentences))
    print(average_number_of_syllables(sentences))
    print(average_number_of_characters(sentences))
    print(count_punctuation(full_text))

if __name__ == '__main__':
    main()
