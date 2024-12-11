import numpy as np


def read_file_timetable(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.readlines()

        professors = {}
        classrooms = []
        groups = {}
        constraints = {'hard': [], 'soft': []}
        week_days = []
        time_slots = []
        courses = []

        current_section = None
        current_professor = None
        current_group = None

        for line in content:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Detectam sectiunea curenta in functie de titlu
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

            # Prelucrarea in functie de sectiunea curenta
            if current_section == 'courses':
                if ':' in line:  # Evităm secțiunile titlu, de exemplu "Cursuri:"
                    continue
                if ' - ' in line:  # Verificăm dacă linia conține informații despre cursuri
                    course_name, professor = line.split(' - ')
                    course_name = course_name.strip()
                    professor = professor.strip()
                    courses.append(f"{course_name} ({professor})")
                    if professor not in professors:
                        professors[professor] = {'courses': [], 'constraints': []}
                    professors[professor]['courses'].append(course_name)

            elif current_section == 'professors':
                if line == 'Profesori:':
                    continue
                if line.endswith(':'):
                    current_professor = line.split(':')[0].strip()
                elif line.strip().startswith("-"):
                    if 'Indisponibil' in line or 'Preferinta' in line:
                        constraint = line.strip()[2:]
                        professors[current_professor]['constraints'].append(constraint)

            elif current_section == 'classrooms':
                if line == 'Sali:':  # Titlul secțiunii
                    continue
                classrooms.append(line)

            elif current_section == 'groups':
                if line == 'Grupe:':  # Titlul secțiunii
                    continue
                if line.endswith(':'):
                    current_group = line.split(':')[0].strip()
                    groups[current_group] = []
                elif current_group:
                    course_list = [course.strip() for course in line.split(',')]
                    groups[current_group].extend(course_list)

            elif current_section == 'week_days':
                week_days = [day.strip() for day in line.split(',')]

            elif current_section == 'time_slots':
                time_slots = [time.strip() for time in line.split(',')]

            elif current_section == 'constraints_hard':
                constraints['hard'].append(line)

            elif current_section == 'constraints_soft':
                constraints['soft'].append(line)

        return courses, professors, classrooms, groups, constraints, week_days, time_slots
    except FileNotFoundError:
        print(f"Fișierul '{file}' nu a fost găsit.")
    except Exception as e:
        print(f"A apărut o eroare: {e}")
