from ReadFFile import read_file_timetable
from ReadFPrompt import read_prompt_timetable
from collections import deque
import time
import numpy as np

def initialize_csp(courses, classrooms, days, time_slots):
    csp = {
        'variables': courses,
        'domains': {course: [(d, t, r) for d in days for t in time_slots for r in classrooms] for course in courses},
        'constraints': {},
        'neighbors': {},
        'arcs': []
    }

    # Generez arcele si lista vecinilor pentru fiecare curs
    for xi in courses:
        csp['neighbors'][xi] = [xj for xj in courses if xj != xi]
        for xj in courses:
            csp['arcs'].append((xi, xj))
    return csp

def satisfies_constraint(x, y, xi, xj, constraints):
    # Verific daca 2 valori ale anumitor variabile respecta toate constrangerile pentru variabilele xi si xj
    for constraint in constraints.get((xi, xj), []):
        if not constraint(x, y):
            return False
    return True

def remove_inconsistent_values(csp, xi, xj):
    removed = False

    for x in csp['domains'][xi]:
        consistent_found = False
        for y in csp['domains'][xj]:
            if satisfies_constraint(x, y, xi, xj, csp['constraints']):
                consistent_found = True
                break

        if not consistent_found:
            print(f"[DEBUG] Elimin valoarea {x} din domeniul lui {xi} pentru ca nu am gasit nicio valoare consistenta in domeniul lui {xj}")
            csp['domains'][xi].remove(x)
            removed = True

    return removed

def AC3(csp):
    # Aplic algoritmul AC3 pentru a reduce domeniile variabilelor prin eliminarea valorilor inconsistente
    queue = deque(csp['arcs'])
    print(f"[DEBUG] Arcele initiale in coada: {queue}")

    while queue:
        xi, xj = queue.popleft()
        print(f"Se prelucreaza arcul ({xi},{xj})")
        if remove_inconsistent_values(csp, xi, xj):
            # Adăugam in coada toate arcele (xk, xi), unde xk sunt vecinii lui xi
            for xk in csp['neighbors'][xi]:
                if xk != xj:
                    queue.append((xk, xi))

def is_assignment_valid(course, prof_index, group, day_index, time_index, room_index, timetable, availability):
    # timetable- matricea de disponibilitate a salilor
    # availability- matricea de disponibilitate a profesorilor
    # Verifica daca asignarea este valida in orar
    if timetable[day_index][time_index][room_index] != "":
        return False
    if availability[day_index][time_index][prof_index] != 0:
        return False
    for room in timetable[day_index][time_index]:
        if f" - {prof_index}" in room:
            return False
        if f"({group})" in room:
            return False
    return True

def backtrack(csp, timetable, remaining_courses, professors, classrooms, zile, intervale, availability, professor_indices, preferences):
    if not remaining_courses:
        print("[DEBUG] Solutie gasita!")
        return True

    current_course = remaining_courses[0]
    remaining_courses_copy = remaining_courses[1:]

    if ' (' in current_course:
        course_name, group = current_course.split(' (')
        group = group[:-1]
    else:
        print(f"[ERROR] Formatul cursului {current_course} este invalid")
        return backtrack(csp, timetable, remaining_courses_copy, professors, classrooms, zile, intervale, availability, professor_indices, preferences)

    print(f"[DEBUG] Incercam sa asignam {current_course}")

    for prof, info in professors.items():
        if course_name in info['courses']:
            prof_idx = professor_indices[prof]

            for day_idx, time_idx, room_idx in csp['domains'][current_course]:
                if is_assignment_valid(course_name, prof_idx, group, day_idx, time_idx, room_idx, timetable, availability):
                    timetable[day_idx][time_idx][room_idx] = f"{course_name} ({group}) - {prof}"
                    print(f"[DEBUG] Cursul {course_name} predat de {prof} asignat {zile[day_idx]} {intervale[time_idx]} in {classrooms[room_idx]}")
                    if backtrack(csp, timetable, remaining_courses_copy, professors, classrooms, zile, intervale, availability, professor_indices, preferences):
                        return True
                    timetable[day_idx][time_idx][room_idx] = ""
                    print(f"[DEBUG] Backtracking after {course_name} assignment.")

    return False

def display_schedule(timetable, zile, intervale, classrooms):
    print("\nOrarul generat:")
    for day_idx, day in enumerate(zile):
        print(f"\n{day}:")
        for time_idx, interval in enumerate(intervale):
            print(f"  {interval}:")
            for room_idx, room in enumerate(classrooms):
                event = timetable[day_idx][time_idx][room_idx]
                if event:
                    print(f"    {room}: {event}")
                else:
                    print(f"    {room}: -")

def main():
    print("Introduceti metoda de citire a datelor de intrare")
    choice = input("Citire prompt (1) Citire fișier (2):  ")
    if choice == "1":
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_prompt_timetable()
    elif choice == "2":
        file_name = input("Introduceti numele fisierului de intrare: ")
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_file_timetable(file_name)
    else:
        print("Optiune invalida!")
        return

    # Valorile implicite daca zilele sau intervalele nu sunt furnizate
    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00', '18:00-20:00']

    # Initializare orar si disponibilitatea profesorilor
    timetable = [[["" for _ in classrooms] for _ in intervale] for _ in zile]
    professor_indices = {prof: i for i, prof in enumerate(professors.keys())}
    availability = np.zeros((len(zile), len(intervale), len(professors)), dtype=int)

    # Parsare constrangeri (disponibilitate si preferinte)
    preferences = {}
    for prof, info in professors.items():
        for constraint in info['constraints']:
            if 'Indisponibil' in constraint:
                parts = constraint.split(' ')
                zi = parts[1]
                interval = ' '.join(parts[2:])
                zi_idx = zile.index(zi)
                interval_idx = intervale.index(interval)
                availability[zi_idx][interval_idx][professor_indices[prof]] = 1
            elif 'Preferinta' in constraint:
                parts = constraint.split(' ')
                zi = parts[1]
                interval = ' '.join(parts[2:])
                zi_idx = zile.index(zi)
                interval_idx = intervale.index(interval)
                preferences.setdefault(prof, []).append((zi_idx, interval_idx))

    # Initializare CSP
    csp = initialize_csp(courses, list(range(len(classrooms))), list(range(len(zile))), list(range(len(intervale))))

    # Procesare constrangeri suplimentare
    for constraint in constraints:
        if constraint == 'Unicitate_sala':
            csp['constraints']['unique_room'] = True
        elif constraint == 'Unicitate_profesor':
            csp['constraints']['unique_professor'] = True
        elif constraint == 'Unicitate_grupa':
            csp['constraints']['unique_group'] = True
        elif constraint == 'Maxim_8_ore_studenti':
            csp['constraints']['max_hours'] = 8
        elif constraint == 'Cursuri_inainte_seminarii':
            csp['constraints']['course_before_seminar'] = True

    # Aplicarea AC-3 pentru reducerea domeniilor
    AC3(csp)

    # Rezolvarea folosind backtracking
    start_time = time.time_ns()
    if backtrack(csp, timetable, courses, professors, classrooms, zile, intervale, availability, professor_indices, preferences):
        display_schedule(timetable, zile, intervale, classrooms)
    else:
        print("Nu am putut gasi o solutie valida pentru orar.")
    end_time = time.time_ns()

    print(f"Timp de executie: {(end_time - start_time) / 1_000_000:.2f} ms")

if __name__ == "__main__":
    main()
