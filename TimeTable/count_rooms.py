def count_rooms(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    is_rooms_section = False
    rooms = []
    for line in lines:
        if "Sali:" in line:
            is_rooms_section = True
            continue
        if is_rooms_section:
            if line.strip() == "":
                break
            rooms.append(line.strip())

    return f"Număr de săli disponibile: {len(rooms)}"
