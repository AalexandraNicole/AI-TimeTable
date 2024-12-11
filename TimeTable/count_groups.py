def count_groups(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    is_groups_section = False
    groups = []
    for line in lines:
        if "Grupe:" in line:
            is_groups_section = True
            continue
        if is_groups_section:
            if line.strip() == "":
                break
            if ":" in line:
                groups.append(line.split(":")[0].strip())

    return f"Număr de grupe: {len(groups)}"
