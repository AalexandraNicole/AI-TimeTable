import numpy as np


def read_file_timetable(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.readlines()

    courses = []
    professors = {}
    classrooms = []
    groups = {}
    constraints = {'hard': [], 'soft': []}
    week_days = []
    time_slots = []

    current_section = None
    current_professor = None

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
        elif 'Zile_saptamana' in line:
            current_section = 'week_days'
        elif 'Intervale_orare' in line:
            current_section = 'time_slots'
        elif 'Constrangeri_hard' in line:
            current_section = 'constraints_hard'
        elif 'Constrangeri_soft' in line:
            current_section = 'constraints_soft'
        elif 'Program_initial_sali' in line:
            current_section = 'initial_schedule'

        if current_section == 'courses':
            if ':' in line:
                continue
            courses.append(line)
        elif current_section == 'professors':
            if line.endswith(':'):  # Aici se identifică numele profesorului
                current_professor = line.split(':')[0].strip()  # Obține numele profesorului
                professors[current_professor] = {'courses': [], 'constraints': []}  # Inițializăm profesorul
            elif current_professor:
                if line.startswith('Constrangeri'):  # Aici încep constrângerile
                    continue  # Ignorăm linia cu "Constrangeri:"
                elif line.startswith('-'):  # Aici se adaugă constrângerile
                    constraint = line[1:].strip()  # Eliminăm primul caracter '-' și spațiile
                    professors[current_professor]['constraints'].append(constraint)  # Adaugă constrângerea
                elif line.startswith('Curs'):  # Aici se adaugă cursurile
                    course_list = line.split('-')[1].strip().split(',')  # Obține cursurile
                    professors[current_professor]['courses'].extend([course.strip() for course in course_list])

        elif current_section == 'classrooms':
            classrooms.append(line)
        elif current_section == 'groups':
            if ':' in line:
                group, group_courses = line.split(':', 1)
                groups[group.strip()] = [c.strip() for c in group_courses.split(',')]
        elif current_section == 'week_days':
            week_days = [day.strip() for day in line.split(',')]
        elif current_section == 'time_slots':
            time_slots = [time.strip() for time in line.split(',')]
        elif current_section == 'constraints_hard':
            constraints['hard'].append(line)
        elif current_section == 'constraints_soft':
            constraints['soft'].append(line)

    first_key = next(iter(professors))  # Obține cheia primului element
    professors.pop(first_key)
    return courses, professors, classrooms, groups, constraints, week_days, time_slots


def read_prompt_timetable():
    courses = []
    professors = {}
    classrooms = []
    groups = {}
    constraints = {'hard': [], 'soft': []}
    week_days = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    time_slots = ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00', '18:00-20:00']

    courses_number = int(input("Introduceți numărul de cursuri: "))
    for _ in range(courses_number):
        course = input("Introduceți denumirea cursului: ")
        courses.append(course)

    prof_numbers = int(input("Introduceți numărul de profesori: "))
    for _ in range(prof_numbers):
        professor = input("Introduceți numele profesorului: ")
        professors[professor] = {'constraints': [], 'courses': []}

        add_courses = input(f"Doriți să adăugați cursuri pentru {professor}? (da/nu): ").lower()
        if add_courses == 'da':
            while True:
                course = input(f"Introduceți cursul pentru {professor} (scrieți 'stop' pentru a opri): ")
                if course.lower() == 'stop':
                    break
                professors[professor]['courses'].append(course)

        add_constraints = input(f"Doriți să adăugați constrângeri pentru {professor}? (da/nu): ").lower()
        if add_constraints == 'da':
            while True:
                constraint = input(f"Introduceți constrângerea pentru {professor} (scrieți 'stop' pentru a opri): ")
                if constraint.lower() == 'stop':
                    break
                professors[professor]['constraints'].append(constraint)

    rooms_number = int(input("Introduceți numărul de săli: "))
    for _ in range(rooms_number):
        room = input("Introduceți denumirea sălii: ")
        classrooms.append(room)

    group_numbers = int(input("Introduceți numărul de grupe: "))
    for _ in range(group_numbers):
        group = input("Introduceți denumirea grupei: ")
        group_courses = input(f"Introduceți cursurile pentru grupa {group}, separate prin virgulă: ")
        groups[group] = [c.strip() for c in group_courses.split(',')]

    hard_constraints_number = int(input("Introduceți numărul de constrângeri hard: "))
    for _ in range(hard_constraints_number):
        hard_constraint = input("Introduceți o constrângere hard: ")
        constraints['hard'].append(hard_constraint)

    soft_constraints_number = int(input("Introduceți numărul de constrângeri soft: "))
    for _ in range(soft_constraints_number):
        soft_constraint = input("Introduceți o constrângere soft: ")
        constraints['soft'].append(soft_constraint)

    return courses, professors, classrooms, groups, constraints, week_days, time_slots


def main():
    choice = input("Doriți să introduceți datele de la prompt (1) sau dintr-un fișier (2)? Introduceți 1 sau 2: ")

    if choice == '1':
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_prompt_timetable()
    elif choice == '2':
        file_name = input("Introduceți numele fișierului: ")
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_file_timetable(file_name)
    else:
        print("Opțiune invalidă!")
        return

    print("\nCursuri:", courses)
    print("Profesori:", professors)
    print("Săli:", classrooms)
    print("Grupe și cursuri:", groups)
    print("Zile:",week_days)
    print("Intervale:", time_slots)
    print("Constrângeri:", constraints)

    # Inițializarea matricelor
    numar_cursuri = len(courses)
    numar_profesori = len(professors)
    numar_grupe = len(groups)
    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Viner']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00',
                                               '18:00-20:00']

    # Matricea de disponibilitate a profesorilor
    matrice_disponibilitate = [[[0 for _ in range(len(professors))] for _ in range(len(intervale))] for _ in
                               range(len(zile))]

    for i, (prof, info) in enumerate(professors.items()):
        for constraint in info['constraints']:
            if 'Indisponibil' in constraint:
                # Exemplu: Indisponibil: Luni 8:00-10:00
                parts = constraint.split(' ')
                zi = parts[1].strip()
                interval = ' '.join(parts[2:]).strip()  # Restul este intervalul, curățat

                print(f"Verificăm zi: '{zi}' și interval: '{interval}'")  # Debugging

                # Asigură-te că ziua și intervalul nu au spații suplimentare
                try:
                    zi_index = zile.index(zi)  # Găsește indexul zilei
                    interval_index = intervale.index(interval)  # Găsește indexul intervalului

                    matrice_disponibilitate[zi_index][interval_index][i] = 1  # 1 înseamnă indisponibil
                except ValueError as e:
                    print(f"Error: {e}")
                    print(f"Zi '{zi}' nu se găsește în lista zilelor.")

    # Matricea de alocare a cursurilor către studenți
    matrice_grupe = np.zeros((numar_grupe, numar_cursuri), dtype=int)

    for i, (group, group_courses) in enumerate(groups.items()):
        for course in group_courses:
            if course in courses:
                course_index = courses.index(course)
                matrice_grupe[i][course_index] = 1  # Grupa are acest curs

    # Matricea de alocare a cursurilor către profesori
    matrice_profesori = np.zeros((numar_profesori, numar_cursuri), dtype=int)

    for i, (prof, info) in enumerate(professors.items()):
        for course in info['courses']:
            if course in courses:
                course_index = courses.index(course)
                matrice_profesori[i][course_index] = 1  # Profesorul predă acest curs

    # Afișăm matricile
    print("\nMatricea de disponibilitate a profesorilor:")
    print(matrice_disponibilitate)

    print("\nMatricea de alocare a cursurilor către studenți:")
    print(matrice_grupe)

    print("\nMatricea de alocare a cursurilor către profesori:")
    print(matrice_profesori)


if __name__ == "__main__":
    main()
