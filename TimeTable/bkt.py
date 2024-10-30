import numpy as np
from ReadFFile import read_file_timetable
from ReadFPrompt import read_prompt_timetable

def is_assignment_valid(course, professor, day_index, time_index, room_index, timetable, constraints, availability_matrix):
    # Verificare de unicitate pentru curs într-o sală
    if any(timetable[day_index][time_index][r] != "" and course in timetable[day_index][time_index][r]
           for r in range(len(timetable[day_index][time_index]))):
        return False

    # Verificare de unicitate pentru profesor
    for t in timetable[day_index][time_index]:
        if t and f" - {professor}" in t:
            return False

    # Verificare de disponibilitate a profesorului
    if availability_matrix[day_index][time_index][professor]:
        return False

    # Verificare dacă profesorul este deja asignat la un alt curs în același interval orar
    for r in range(len(timetable[day_index][time_index])):
        if timetable[day_index][time_index][r] and f" - {professor}" in timetable[day_index][time_index][r]:
            return False

    return True

def backtrack(timetable, courses, professors, classrooms, zile, intervale, constraints, availability_matrix):
    for day_index in range(len(zile)):
        for time_index in range(len(intervale)):
            for course in courses:
                for room_index, room in enumerate(classrooms):
                    professor = None
                    for prof_index, (prof, info) in enumerate(professors.items()):
                        if course in info['courses']:
                            professor = prof_index
                            break

                    if professor is None:
                        continue

                    if timetable[day_index][time_index][room_index] == "" and is_assignment_valid(
                            course, professor, day_index, time_index, room_index, timetable, constraints,
                            availability_matrix):
                        timetable[day_index][time_index][room_index] = f"{course} - {prof}"

                        if all(all(all(cell != "" for cell in row) for row in day) for day in timetable):
                            return True

                        if backtrack(timetable, courses, professors, classrooms, zile, intervale, constraints,
                                     availability_matrix):
                            return True

                        timetable[day_index][time_index][room_index] = ""
    return False

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

    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00',
                                               '18:00-20:00']

    timetable = [[["" for _ in classrooms] for _ in intervale] for _ in zile]

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

    if backtrack(timetable, courses, professors, classrooms, zile, intervale, constraints, availability_matrix):
        print("\nProgramul rezultat:")
        for day_index, day in enumerate(zile):
            print(f"{day}:")
            for time_index, interval in enumerate(intervale):
                print(f"  {interval}:")
                for room_index, room in enumerate(classrooms):
                    course = timetable[day_index][time_index][room_index]
                    if course:
                        print(f"    {room}: {course}")
                    else:
                        print(f"    {room}: -")
    else:
        print("Nu a fost găsită o soluție validă.")

if __name__ == "__main__":
    main()