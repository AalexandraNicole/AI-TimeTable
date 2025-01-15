from collections import Counter
import re


def stylometric_analysis(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    words = re.findall(r'\b\w+\b', text)
    num_words = len(words)
    num_chars = len(text)
    word_frequencies = Counter(words)

    # Construirea rezultatelor ca text
    result = []
    result.append(f"Lungime în caractere: {num_chars}")
    result.append(f"Lungime în cuvinte: {num_words}")
    result.append("Frecvența cuvintelor (primele 10):")
    for word, count in word_frequencies.most_common(10):
        result.append(f"  {word}: {count}")

    return "\n".join(result)
