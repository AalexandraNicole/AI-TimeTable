# timetable.py

from ac3_bkt import initialize_csp, AC3, backtrack, is_assignment_valid, display_schedule
import numpy as np
import time


def run_scheduler(courses, professors, classrooms, constraints, week_days, time_slots, timetable, professor_indices,
                  availability, preferences):
    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00',
                                               '18:00-20:00']

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

    # Backtracking for solution
    start_time = time.time_ns()
    if backtrack(csp, timetable, courses, professors, classrooms, zile, intervale, availability, professor_indices, preferences):
        return timetable
    else:
        return "Nu am putut gasi o solutie valida pentru orar."
