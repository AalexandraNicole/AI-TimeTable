from langdetect import detect


def detect_file_language(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    language = detect(content)
    return f"Limbă detectată: {language}"
