def read_file_timetable(file):
    with open(file, 'r') as f:
        content = f.readlines()

    courses = []
    professors = {}
    classrooms = []
    groups = {}
    time_intervals = {}
    constraints = {'hard': [], 'soft': []}

    current_section = None

    for line in content:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if 'Cursuri' in line:
            current_section = 'courses'
        elif 'Profesori' in line:
            current_section = 'professors'
        elif 'Sali' in line:
            current_section = 'classrooms'
        elif 'Grupe' in line:
            current_section = 'groups'
        elif 'Intervale_orare' in line:
            current_section = 'time_intervals'
        elif 'Constrangeri' in line:
            if 'hard' in line:
                current_section = 'constraints_hard'
            else:
                current_section = 'constraints_soft'

        # Adăugăm date în funcție de secțiune
        if current_section == 'courses':
            courses.append(line)
        elif current_section == 'professors':
            if ':' in line:
                profesor, rest = line.split(':')
                professors[profesor.strip()] = {'constraints': []}
            elif 'Indisponibil' in line or 'Preferinta' in line:
                professors[profesor.strip()]['constraints'].append(line.strip())
        elif current_section == 'classrooms':
            classrooms.append(line)
        elif current_section == 'groups':
            if ':' in line:
                group, group_courses = line.split(':')
                groups[group.strip()] = [c.strip() for c in group_courses.split(',')]
        elif current_section == 'constraints_hard':
            constraints['hard'].append(line)
        elif current_section == 'constraints_soft':
            constraints['soft'].append(line)

    return courses, professors, classrooms, groups, constraints


def read_prompt_timetable():
    courses = []
    professors = {}
    classrooms = []
    groups = {}
    constraints = {'hard': [], 'soft': []}

    # Citire cursuri
    courses_number = int(input("Introduceți numărul de cursuri: "))
    for _ in range(courses_number):
        course = input("Introduceți denumirea cursului: ")
        courses.append(course)

    # Citire profesori și constrângeri
    prof_numbers = int(input("Introduceți numărul de profesori: "))
    for _ in range(prof_numbers):
        professor = input("Introduceți numele profesorului: ")
        professors[professor] = {'constraints': []}

        # Adăugarea constrângerilor pentru profesori
        add_constraints = input(f"Doriți să adăugați constrângeri pentru {professor}? (da/nu): ").lower()
        if add_constraints == 'da':
            while True:
                constraint = input(f"Introduceți constrângerea pentru {professor} (scrieți 'stop' pentru a opri): ")
                if constraint.lower() == 'stop':
                    break
                professors[professor]['constraints'].append(constraint)

    # Citire săli
    rooms_number = int(input("Introduceți numărul de săli: "))
    for _ in range(rooms_number):
        room = input("Introduceți denumirea sălii: ")
        classrooms.append(room)

    # Citire grupe și cursuri aferente
    group_numbers = int(input("Introduceți numărul de grupe: "))
    for _ in range(group_numbers):
        groupe = input("Introduceți denumirea grupei: ")
        group_courses = input(f"Introduceți cursurile pentru grupa {groupe}, separate prin virgulă: ")
        groups[groupe] = [c.strip() for c in group_courses.split(',')]

    # Citire constrângeri hard și soft
    hard_constraints_number = int(input("Introduceți numărul de constrângeri hard: "))
    for _ in range(hard_constraints_number):
        hard_constraint = input("Introduceți o constrângere hard: ")
        constraints['hard'].append(hard_constraint)

    soft_constraints_number = int(input("Introduceți numărul de constrângeri soft: "))
    for _ in range(soft_constraints_number):
        soft_constraints = input("Introduceți o constrângere soft: ")
        constraints['soft'].append(soft_constraints)

    return courses, professors, classrooms, groups, constraints


# Exemplu de utilizare pentru prompt
courses, professors, classrooms, groups, constraints = read_prompt_timetable()

# Exemplu de utilizare pentru fișier
#courses, professors, classrooms, groups, constraints = read_file_timetable('orar.txt')

# Afișăm informațiile citite
print("\nCursuri:", courses)
print("Profesori și constrângeri:", professors)
print("Săli:", classrooms)
print("Grupe și cursuri:", groups)
print("Constrângeri:", constraints)
