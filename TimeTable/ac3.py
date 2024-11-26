from ReadFFile import read_file_timetable
from ReadFPrompt import read_prompt_timetable
from collections import deque
import numpy as np


def initialize_csp(courses, classrooms, days, time_slots):
    csp = {
        'variables': courses,
        'domains': {course: [(d, t, r) for d in days for t in time_slots for r in classrooms] for course in courses},
        'constraints': {},
        'neighbors': {},
        'arcs': []
    }

    # Generez arcele și lista vecinilor pentru fiecare curs
    for xi in courses:
        csp['neighbors'][xi] = [xj for xj in courses if xj != xi]
        for xj in courses:
            csp['arcs'].append((xi, xj))
    return csp


def satisfies_constraint(x, y, xi, xj, constraints):
    # Verific dacă 2 valori ale anumitor variabile respectă toate constrângerile pentru variabilele xi și xj
    for constraint in constraints.get((xi, xj), []):
        if not constraint(x, y):
            return False
    return True


def remove_inconsistent_values(csp, xi, xj):
    removed = False

    for x in csp['domains'][xi][:]:  # Iterez printr-o copie a domeniului
        consistent_found = False
        for y in csp['domains'][xj]:
            if satisfies_constraint(x, y, xi, xj, csp['constraints']):
                consistent_found = True
                break

        if not consistent_found:
            print(
                f"[DEBUG] Elimin valoarea {x} din domeniul lui {xi} pentru că nu am găsit nicio valoare consistentă în domeniul lui {xj}")
            csp['domains'][xi].remove(x)
            removed = True

    return removed


def AC3(csp):
    # Aplic algoritmul AC3 pentru a reduce domeniile variabilelor prin eliminarea valorilor inconsistente
    queue = deque(csp['arcs'])
    print(f"[DEBUG] Arcele inițiale în coadă: {queue}")

    while queue:
        xi, xj = queue.popleft()
        print(f"Se prelucrează arcul ({xi},{xj})")
        if remove_inconsistent_values(csp, xi, xj):
            # Adăugăm în coadă toate arcele (xk, xi), unde xk sunt vecinii lui xi
            for xk in csp['neighbors'][xi]:
                if xk != xj:
                    queue.append((xk, xi))


def display_schedule_from_ac3(csp, zile, intervale, classrooms):
    print("\nOrarul rezultat din AC-3:")
    timetable = [[["" for _ in classrooms] for _ in intervale] for _ in zile]

    for course, domain in csp['domains'].items():
        if len(domain) == 1:  # Dacă domeniul are o singură valoare, cursul poate fi programat
            day_idx, time_idx, room_idx = domain[0]
            timetable[day_idx][time_idx][room_idx] = course
        elif len(domain) > 1:
            print(f"[WARN] Domeniul pentru {course} nu este unic: {domain}")
        else:
            print(f"[ERROR] Domeniul pentru {course} este gol!")

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
    print("Introduceți metoda de citire a datelor de intrare")
    choice = input("Citire prompt (1) Citire fișier (2):  ")
    if choice == "1":
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_prompt_timetable()
    elif choice == "2":
        file_name = input("Introduceți numele fișierului de intrare: ")
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_file_timetable(file_name)
    else:
        print("Opțiune invalidă!")
        return

    # Valorile implicite dacă zilele sau intervalele nu sunt furnizate
    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00',
                                               '18:00-20:00']

    classrooms_indices = list(range(len(classrooms)))
    zile_indices = list(range(len(zile)))
    intervale_indices = list(range(len(intervale)))

    # Initializare CSP
    csp = initialize_csp(courses, classrooms_indices, zile_indices, intervale_indices)

    # Procesare constrângeri din input
    for group, group_courses in groups.items():
        for course1 in group_courses:
            for course2 in group_courses:
                if course1 != course2:
                    csp['constraints'].setdefault((course1, course2), []).append(lambda x, y: x != y)

    for prof, info in professors.items():
        for course1 in info['courses']:
            for course2 in info['courses']:
                if course1 != course2:
                    csp['constraints'].setdefault((course1, course2), []).append(lambda x, y: x != y)

    # Aplicarea AC-3
    AC3(csp)

    # Afisarea orarului rezultat
    display_schedule_from_ac3(csp, zile, intervale, classrooms)


if __name__ == "__main__":
    main()
