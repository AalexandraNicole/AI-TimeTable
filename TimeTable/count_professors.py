def count_professors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    is_professors_section = False
    professors = []
    for line in lines:
        if "Profesori:" in line:
            is_professors_section = True
            continue
        if is_professors_section:
            if line.strip() == "":
                break
            if len(line.strip()) == 2 and line.strip()[1] == ":" and line.strip()[0].isupper():
                professors.append(line.strip()[0])

    return f"Număr de profesori: {len(professors)}"
