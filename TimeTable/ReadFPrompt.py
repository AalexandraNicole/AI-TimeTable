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
