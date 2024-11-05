import numpy as np
from collections import deque
from ReadFFile import read_file_timetable
from ReadFPrompt import read_prompt_timetable


def ac3(csp):
    # algoritmul AC-3 pentru a asigura consistența arcelor
    queue = deque(csp['arcs'])

    while queue:
        (xi, xj) = queue.popleft()
        if remove_inconsistent_values(csp, xi, xj):
            for xk in csp['neighbors'][xi]:
                queue.append((xk, xi))


def remove_inconsistent_values(csp, xi, xj):
    # elimină valorile inconsistente din domeniul lui xi
    removed = False
    for x in csp['domains'][xi][:]:
        if not any(satisfies_constraint(x, y, xi, xj, csp['constraints']) for y in csp['domains'][xj]):
            csp['domains'][xi].remove(x)
            removed = True
    return removed


def satisfies_constraint(x, y, xi, xj, constraints):
    # verifică dacă valorile x și y satisfac constrângerile dintre xi și xj
    for constraint in constraints.get((xi, xj), []):
        if not constraint(x, y):
            return False
    return True


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
    print("Zile:", week_days)
    print("Intervale:", time_slots)
    print("Constrângeri:", constraints)

    csp = {
        'variables': courses,
        'domains': {course: time_slots[:] for course in courses},
        'constraints': {},
        'neighbors': {course: [] for course in courses},
        'arcs': []
    }

    for group, group_courses in groups.items():
        for course in group_courses:
            if course in csp['variables']:
                for other_course in group_courses:
                    if other_course != course:
                        csp['constraints'].setdefault((course, other_course), []).append(lambda x, y: x != y)
                        csp['neighbors'][course].append(other_course)
                        csp['neighbors'][other_course].append(course)
                        csp['arcs'].append((course, other_course))
                        csp['arcs'].append((other_course, course))

    for prof, info in professors.items():
        for course in info['courses']:
            if course in csp['variables']:
                for other_course in info['courses']:
                    if other_course != course:
                        csp['constraints'].setdefault((course, other_course), []).append(lambda x, y: x != y)
                        csp['neighbors'][course].append(other_course)
                        csp['neighbors'][other_course].append(course)
                        csp['arcs'].append((course, other_course))
                        csp['arcs'].append((other_course, course))

    ac3(csp)

    for var in csp['variables']:
        print(f"Domain of {var}: {csp['domains'][var]}")


if __name__ == "__main__":
    main()
