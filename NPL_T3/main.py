import nltk
from nltk.corpus import wordnet as wn
from langdetect import detect
from nltk.probability import FreqDist
import random

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def read_file_into_string(filename):
    with open(f'{filename}.txt', 'r', encoding='utf-8') as f:
        return f.read()


def replace_with_synonyms_or_hypernyms(text, replacement_rate=0.2):
    """Înlocuiește cel puțin 20% din cuvintele textului cu sinonime, hipernime sau antonime negate."""
    tokens = nltk.word_tokenize(text)
    new_tokens = []

    for token in tokens:
        if random.random() > replacement_rate or not token.isalpha():
            new_tokens.append(token)
            continue

        synosets = wn.synsets(token)
        if synosets:
            # Sinonime
            synonyms = set(lemma.name().replace('_', ' ') for synset in synosets for lemma in synset.lemmas() if lemma.name().lower() != token.lower())

            # Hipernime
            hypernyms = set(hypernym.name().split('.')[0].replace('_', ' ') for synset in synosets for hypernym in synset.hypernyms())

            # Antonyme negate
            antonyms = set("nu " + ant.name().replace('_', ' ') for synset in synosets for lemma in synset.lemmas() for ant in lemma.antonyms())

            # Alegerea unui înlocuitor disponibil
            replacements = list(synonyms | hypernyms | antonyms)
            if replacements:
                new_tokens.append(random.choice(replacements))
            else:
                new_tokens.append(token)
        else:
            new_tokens.append(token)

    # Asigurarea unei rate minime de înlocuire
    if len(new_tokens) > 0 and len(new_tokens) - len(tokens) < replacement_rate * len(tokens):
        additional_replacements = int(replacement_rate * len(tokens) - (len(new_tokens) - len(tokens)))
        indices = [i for i, token in enumerate(tokens) if token.isalpha() and new_tokens[i] == token]
        random.shuffle(indices)
        for i in indices[:additional_replacements]:
            synosets = wn.synsets(tokens[i])
            if synosets:
                synonyms = set(lemma.name().replace('_', ' ') for synset in synosets for lemma in synset.lemmas() if lemma.name().lower() != tokens[i].lower())
                hypernyms = set(hypernym.name().split('.')[0].replace('_', ' ') for synset in synosets for hypernym in synset.hypernyms())
                antonyms = set("nu " + ant.name().replace('_', ' ') for synset in synosets for lemma in synset.lemmas() for ant in lemma.antonyms())
                replacements = list(synonyms | hypernyms | antonyms)
                if replacements:
                    new_tokens[i] = random.choice(replacements)

    return ' '.join(new_tokens)

def analyze_text(text):
    # detectarea limbii
    try:
        language = detect(text)
    except Exception as e:
        language = "Limba nedetectata: " + str(e)

    # tokenizare
    tokens = nltk.word_tokenize(text)
    words = [token for token in tokens if token.isalpha()]

    # calculam innformatiile stilometrice
    num_chars = len(text)
    num_words = len(words)
    num_unique_words = len(set(words))
    freq_dist = FreqDist(words)

    # Afișarea rezultatelor
    print("\nInformații despre text:")
    print(f"Limbă detectată: {language}")
    print(f"Număr de caractere: {num_chars}")
    print(f"Număr de cuvinte: {num_words}")
    print(f"Număr de cuvinte unice: {num_unique_words}")
    print("\nFrecvența celor mai comune 10 cuvinte:")
    for word, freq in freq_dist.most_common(10):
        print(f"{word}: {freq}")


def main():
    choice = input("Doriti sa introduceti textul de la prompt (1) sau din fisier (2): ")
    if choice == '1':
        text = input("Introdueti textul si apasati Enter: \n")
    elif choice == '2':
        filename = input("Introduceti numele fisierului (fara extensie): ")
        try:
            text = read_file_into_string(filename)
        except FileNotFoundError:
            print("Fisierul nu a fost gasit!")
            return
    else:
        print("Opțiune invalidă!")
        return

    print("\nText modificat:")
    modified_text = replace_with_synonyms_or_hypernyms(text)
    print(modified_text)

    analyze_text(text)


if __name__ == "__main__":
    main()
