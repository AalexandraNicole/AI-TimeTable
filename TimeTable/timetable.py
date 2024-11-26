# bkt_ac3.py

import numpy as np
from collections import deque
import time


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
            csp['domains'][xi].remove(x)
            removed = True

    return removed


def AC3(csp):
    queue = deque(csp['arcs'])

    while queue:
        xi, xj = queue.popleft()
        if remove_inconsistent_values(csp, xi, xj):
            for xk in csp['neighbors'][xi]:
                if xk != xj:
                    queue.append((xk, xi))


def is_assignment_valid(course, prof_index, group, day_index, time_index, room_index, timetable, availability):
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


def backtrack(csp, timetable, remaining_courses, professors, classrooms, zile, intervale, availability,
              professor_indices, preferences):
    if not remaining_courses:
        return True

    current_course = remaining_courses[0]
    remaining_courses_copy = remaining_courses[1:]

    if ' (' in current_course:
        course_name, group = current_course.split(' (')
        group = group[:-1]
    else:
        return backtrack(csp, timetable, remaining_courses_copy, professors, classrooms, zile, intervale, availability,
                         professor_indices, preferences)

    for prof, info in professors.items():
        if course_name in info['courses']:
            prof_idx = professor_indices[prof]

            for day_idx, time_idx, room_idx in csp['domains'][current_course]:
                if is_assignment_valid(course_name, prof_idx, group, day_idx, time_idx, room_idx, timetable,
                                       availability):
                    timetable[day_idx][time_idx][room_idx] = f"{course_name} ({group}) - {prof}"
                    if backtrack(csp, timetable, remaining_courses_copy, professors, classrooms, zile, intervale,
                                 availability, professor_indices, preferences):
                        return True
                    timetable[day_idx][time_idx][room_idx] = ""

    return False


def display_schedule(timetable, zile, intervale, classrooms):
    schedule_str = ""
    for day_idx, day in enumerate(zile):
        schedule_str += f"\n{day}:\n"
        for time_idx, interval in enumerate(intervale):
            schedule_str += f"  {interval}:\n"
            for room_idx, room in enumerate(classrooms):
                event = timetable[day_idx][time_idx][room_idx]
                if event:
                    schedule_str += f"    {room}: {event}\n"
                else:
                    schedule_str += f"    {room}: -\n"
    return schedule_str


def run_scheduler(courses, professors, classrooms, constraints, week_days, time_slots, timetable, professor_indices,
                  availability, preferences):
    # Initializing the CSP and constraints
    csp = initialize_csp(courses, list(range(len(classrooms))), list(range(len(week_days))),
                         list(range(len(time_slots))))

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

    AC3(csp)

    # Backtracking for solution
    start_time = time.time_ns()
    if backtrack(csp, timetable, courses, professors, classrooms, week_days, time_slots, availability,
                 professor_indices, preferences):
        return timetable
    else:
        return "Nu am putut gasi o solutie valida pentru orar."
