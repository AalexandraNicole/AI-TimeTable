def count_courses(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    is_courses_section = False
    total_courses = 0
    for line in lines:
        if "Cursuri:" in line:
            is_courses_section = True
            continue
        if is_courses_section:
            if line.strip() == "":
                break
            total_courses += 1

    return f"Număr total de cursuri: {total_courses}"
