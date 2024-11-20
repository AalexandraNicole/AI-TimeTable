import numpy as np
from ReadFFile import read_file_timetable
from ReadFPrompt import read_prompt_timetable

def is_assignment_valid(course, professor_index, group, day_index, time_index, room_index, timetable, availability_matrix):
    # Verificare de unicitate pentru curs într-o sală
    if timetable[day_index][time_index][room_index] != "":
        print(f"[DEBUG] Sala {room_index} este deja ocupată la {day_index} {time_index}")
        return False

    # Verificare de disponibilitate a profesorului
    if availability_matrix[day_index][time_index][professor_index] == 1:
        print(f"[DEBUG] Profesorul {professor_index} nu este disponibil la {day_index} {time_index}")
        return False

    # Verificare de unicitate pentru profesor
    for r in range(len(timetable[day_index][time_index])):
        if timetable[day_index][time_index][r] and f" - {professor_index}" in timetable[day_index][time_index][r]:
            print(f"[DEBUG] Profesorul {professor_index} are deja un curs la {day_index} {time_index}")
            return False

    # Verificare dacă grupul este deja asignat la un alt curs în același interval orar
    for r in range(len(timetable[day_index][time_index])):
        if timetable[day_index][time_index][r] and f"({group})" in timetable[day_index][time_index][r]:
            print(f"[DEBUG] Grupul {group} are deja un curs la {day_index} {time_index}")
            return False

    return True

def backtrack(timetable, remaining_courses, professors, classrooms, zile, intervale, availability_matrix, professor_indices):
    if not remaining_courses:
        return True

    current_course = remaining_courses[0]
    remaining_courses_copy = remaining_courses[1:]

    # Verifică formatul cursului
    if ' (' in current_course:
        course_name, group = current_course.split(' (')
        group = group[:-1]
    else:
        print(f"[ERROR] Format curs invalid: {current_course}")
        return backtrack(timetable, remaining_courses_copy, professors, classrooms, zile, intervale, availability_matrix, professor_indices)

    print(f"[DEBUG] Procesare curs: {current_course} (Grupa: {group})")

    # Iterează prin zile, intervale și săli
    for day_index in range(len(zile)):
        for time_index in range(len(intervale)):
            for room_index, room in enumerate(classrooms):
                for prof, info in professors.items():
                    if course_name in info['courses']:
                        professor_index = professor_indices[prof]

                        if is_assignment_valid(course_name, professor_index, group, day_index, time_index, room_index, timetable, availability_matrix):
                            timetable[day_index][time_index][room_index] = f"{course_name} ({group}) - {prof}"
                            print(f"[DEBUG] Assigned {course_name} ({group}) - {prof} to {zile[day_index]} {intervale[time_index]} in room {room}")

                            # Apel recursiv pentru restul cursurilor
                            if backtrack(timetable, remaining_courses_copy, professors, classrooms, zile, intervale, availability_matrix, professor_indices):
                                return True

                            # Backtrack dacă nu s-a găsit o soluție
                            timetable[day_index][time_index][room_index] = ""
                            print(f"[DEBUG] Backtracked on {course_name} ({group}) - {prof} from {zile[day_index]} {intervale[time_index]} in room {room}")

    print(f"[DEBUG] Unable to schedule course: {current_course}")
    return False

def display_schedule(timetable, zile, intervale, classrooms):
    print("\nProgramul rezultat:")
    for day_index, day in enumerate(zile):
        print(f"\n{day}:")
        for time_index, interval in enumerate(intervale):
            print(f"  {interval}:")
            for room_index, room in enumerate(classrooms):
                course = timetable[day_index][time_index][room_index]
                if course:
                    print(f"    {room}: {course}")
                else:
                    print(f"    {room}: -")

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

    # Adaugă print pentru a verifica datele citite
    print(f"[DEBUG] Cursuri: {courses}")
    print(f"[DEBUG] Profesori: {professors}")
    print(f"[DEBUG] Săli: {classrooms}")
    print(f"[DEBUG] Grupe: {groups}")
    print(f"[DEBUG] Constrângeri: {constraints}")
    print(f"[DEBUG] Zile: {week_days}")
    print(f"[DEBUG] Intervale: {time_slots}")

    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00', '18:00-20:00']

    timetable = [[["" for _ in classrooms] for _ in intervale] for _ in zile]

    # Crează un dicționar pentru indexarea profesorilor
    professor_indices = {prof: i for i, prof in enumerate(professors.keys())}
    print(f"[DEBUG] Indici profesori: {professor_indices}")

    # Crează matricea de disponibilitate a profesorilor
    availability_matrix = np.zeros((len(zile), len(intervale), len(professors)), dtype=int)
    for i, (professor, info) in enumerate(professors.items()):
        for constraint in info['constraints']:
            if 'Indisponibil' in constraint:
                parts = constraint.split(' ')
                zi = parts[1].strip()
                interval = ' '.join(parts[2:]).strip()
                try:
                    zi_index = zile.index(zi)
                    interval_index = intervale.index(interval)
                    availability_matrix[zi_index][interval_index][i] = 1
                except ValueError as e:
                    print(f"Error: {e}")
                    print(f"Zi '{zi}' nu se găsește în lista zilelor.")

    print(f"[DEBUG] Matr. Disponibilitate Profesori:\n{availability_matrix}")

    # Apelează backtracking-ul pentru a plasa cursurile
    if backtrack(timetable, courses, professors, classrooms, zile, intervale, availability_matrix, professor_indices):
        display_schedule(timetable, zile, intervale, classrooms)
    else:
        print("Nu a fost găsită o soluție validă.")
        display_schedule(timetable, zile, intervale, classrooms)

if __name__ == "__main__":
    main()
