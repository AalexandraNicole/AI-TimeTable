import random
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn
from langdetect import detect
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# Citește un fișier și returnează conținutul acestuia
def read_file_into_string(filename):
    with open(f'{filename}.txt', 'r', encoding='utf-8') as f:
        return f.read()

# Înlocuiește cuvinte cu sinonime, hipernime sau antonime negate
def replace_with_synonyms_or_hypernyms(text, replacement_rate=0.2, lang=None):
    if lang is None:
        # Detectează limba dacă nu este furnizată
        lang = detect(text)

    tokens = nltk.word_tokenize(text)
    new_tokens = []

    # Setează cuvântul pentru negare în funcție de limbă
    negation_word = 'nu' if lang == 'ro' else 'not'

    for token in tokens:
        if random.random() > replacement_rate or not token.isalpha():
            new_tokens.append(token)
            continue

        synosets = wn.synsets(token, lang=lang)
        if synosets:
            # Sinonime
            synonyms = set(lemma.name().replace('_', ' ') for synset in synosets for lemma in synset.lemmas(lang) if
                           lemma.name().lower() != token.lower())
            # Hipernime
            hypernyms = set(hypernym.name().split('.')[0].replace('_', ' ') for synset in synosets for hypernym in
                            synset.hypernyms())
            # Antonyme negate
            antonyms = set(
                f"{negation_word} " + ant.name().replace('_', ' ') for synset in synosets for lemma in synset.lemmas(lang) for ant in
                lemma.antonyms())

            replacements = list(synonyms | hypernyms | antonyms)
            if replacements:
                new_tokens.append(random.choice(replacements))
            else:
                new_tokens.append(token)
        else:
            new_tokens.append(token)

    return ' '.join(new_tokens)

# Analiza stilometrică
def stylometric_analysis(text):
    tokens = nltk.word_tokenize(text)
    words = [token for token in tokens if token.isalpha()]
    num_chars = len(text)
    num_words = len(words)
    num_unique_words = len(set(words))
    freq_dist = FreqDist(words)

    result = []
    result.append(f"Lungime în caractere: {num_chars}")
    result.append(f"Lungime în cuvinte: {num_words}")
    result.append(f"Număr de cuvinte unice: {num_unique_words}")
    result.append("\nFrecvența celor mai comune 10 cuvinte:")
    for word, freq in freq_dist.most_common(10):
        result.append(f"{word}: {freq}")

    return '\n'.join(result)

# Extrage cuvintele cheie și generează propozițiile asociate
def extract_keywords_and_generate_sentences(text, num_keywords=5, lang='ron'):
    sentences = sent_tokenize(text)
    stop_words = stopwords.words('english')
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=num_keywords)
    tfidf_matrix = vectorizer.fit_transform(sentences)

    keywords = vectorizer.get_feature_names_out()
    keyword_sentences = {}

    for keyword in keywords:
        for sentence in sentences:
            if keyword.lower() in sentence.lower():
                keyword_sentences[keyword] = sentence
                break

    result = []
    for keyword, sentence in keyword_sentences.items():
        words = word_tokenize(sentence)
        words_filtered = [word for word in words if word.isalpha()]
        random_words = random.sample(words_filtered, min(5, len(words_filtered)))
        random_index = random.randint(0, len(random_words))
        random_words.insert(random_index, keyword)
        new_sentence = ' '.join(random_words)
        result.append(f"Cuvânt cheie: {keyword}")
        result.append(f"Propoziție: {new_sentence}")

    return '\n'.join(result)

# Funcția principală
def main():
    choice = input("Doriți să introduceți textul de la prompt (1) sau din fișier (2): ")
    if choice == '1':
        text = input("Introduceți textul și apăsați Enter: \n")
    elif choice == '2':
        filename = input("Introduceți numele fișierului (fără extensie): ")
        try:
            text = read_file_into_string(filename)
        except FileNotFoundError:
            print("Fișierul nu a fost găsit!")
            return
    else:
        print("Opțiune invalidă!")
        return

    # Detectare limbă
    try:
        language = detect(text)
        print(f"\nLimbă detectată: {language}")
    except Exception as e:
        print(f"\nEroare la detectarea limbii: {e}")
        return

    # Schimbă limba în funcție de detectarea limbii
    lang = 'ron' if language == 'ro' else 'eng'

    # Analiza stilometrică
    print("\nInformații stilometrice:")
    print(stylometric_analysis(text))

    # Generare text alternativ
    print("\nText alternativ:")
    modified_text = replace_with_synonyms_or_hypernyms(text, lang=lang)
    print(modified_text)

    # Extrage cuvintele cheie și generează propoziții
    print("\nCuvinte cheie și propoziții asociate:")
    print(extract_keywords_and_generate_sentences(text, lang=lang))

if __name__ == "__main__":
    main()
