import numpy as np
from collections import deque
from ReadFFile import read_file_timetable
from ReadFPrompt import read_prompt_timetable


def initialize_csp(courses, classrooms, days, time_slots):
    csp = {
        'variables': courses,
        'domains': {course: [(d, t, r) for d in days for t in time_slots for r in classrooms] for course in courses},
        'constraints': {},
        'neighbors': {},
        'arcs': []
    }

    for xi in courses:
        csp['neighbors'][xi] = [xj for xj in courses if xj != xi]
        for xj in courses:
            csp['arcs'].append((xi, xj))
    return csp


def satisfies_constraint(x, y, xi, xj, constraints):
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
            print(
                f"[DEBUG] Elimin valoarea {x} din domeniul lui {xi} pentru ca nu am gasit nicio valoare consistenta in domeniul lui {xj}")
            csp['domains'][xi].remove(x)
            removed = True

    return removed


def ac3(csp):
    queue = deque(csp['arcs'])
    print(f"[DEBUG] Arcele initiale in coada: {queue}")

    while queue:
        xi, xj = queue.popleft()
        # print(f"Se prelucreaza arcul ({xi},{xj})")
        if remove_inconsistent_values(csp, xi, xj):
            for xk in csp['neighbors'][xi]:
                if xk != xj:
                    queue.append((xk, xi))


def get_domains_string(csp, zile, intervale, classrooms):
    result = ""
    for course, domain in csp['domains'].items():
        result += f"Domain of {course}:\n"
        formatted_domain = format_domain(domain, zile, intervale, classrooms)
        for entry in formatted_domain:
            result += f"  - {entry}\n"
        result += "\n"  # Adding a line break after each course's domain
    return result


def format_domain(domain, zile, intervale, classrooms):
    formatted_domain = []
    for day_idx, time_idx, room_idx in domain:
        day = zile[day_idx]
        time = intervale[time_idx]
        room = classrooms[room_idx]
        formatted_domain.append(f"{day} {time} (Room {room})")
    return formatted_domain


def print_domains(csp, zile, intervale, classrooms):
    for course, domain in csp['domains'].items():
        print(f"Domain of {course}:")
        formatted_domain = format_domain(domain, zile, intervale, classrooms)
        for entry in formatted_domain:
            print(f"  - {entry}")
        print()


def main(courses, professors, classrooms, constraints, week_days, time_slots, file_name=None):
    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00',
                                               '18:00-20:00']

    timetable = [[["" for _ in classrooms] for _ in intervale] for _ in zile]
    professor_indices = {prof: i for i, prof in enumerate(professors.keys())}
    availability = np.zeros((len(zile), len(intervale), len(professors)), dtype=int)

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

    csp = initialize_csp(courses, list(range(len(classrooms))), list(range(len(zile))), list(range(len(intervale))))

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

    ac3(csp)

    # Instead of printing, we return the string
    return get_domains_string(csp, zile, intervale, classrooms)


def run_main_from_gui(choice, file_name=None):
    if choice == "1":
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_prompt_timetable()
        return main(courses, professors, classrooms, constraints, week_days, time_slots)
    elif choice == "2" and file_name:
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_file_timetable(file_name)
        return main(courses, professors, classrooms, constraints, week_days, time_slots, file_name)
    else:
        return "Optiune invalida!"


if __name__ == "__main__":
    main()
