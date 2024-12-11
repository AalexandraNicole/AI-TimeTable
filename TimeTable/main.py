import numpy as np
from read_f_file import read_file_timetable
from read_f_prompt import read_prompt_timetable


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

    numar_cursuri = len(courses)
    numar_profesori = len(professors)
    numar_grupe = len(groups)
    zile = week_days if week_days else ['Luni', 'Marti', 'Miercuri', 'Joi', 'Viner']
    intervale = time_slots if time_slots else ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00',
                                               '18:00-20:00']

    matrice_disponibilitate = np.zeros((len(zile), len(intervale), numar_profesori), dtype=int)

    for i, (prof, info) in enumerate(professors.items()):
        for constraint in info['constraints']:
            if 'Indisponibil' in constraint:
                parts = constraint.split(' ')
                zi = parts[1].strip()
                interval = ' '.join(parts[2:]).strip()

                print(f"Verificăm zi: '{zi}' și interval: '{interval}'")

                try:
                    zi_index = zile.index(zi)
                    interval_index = intervale.index(interval)

                    matrice_disponibilitate[zi_index][interval_index][i] = 1
                except ValueError as e:
                    print(f"Error: {e}")
                    print(f"Zi '{zi}' nu se găsește în lista zilelor.")

    matrice_grupe = np.zeros((numar_grupe, numar_cursuri), dtype=int)

    for i, (group, group_courses) in enumerate(groups.items()):
        for course in group_courses:
            if course in courses:
                course_index = courses.index(course)
                matrice_grupe[i][course_index] = 1

    matrice_profesori = np.zeros((numar_profesori, numar_cursuri), dtype=int)

    for i, (prof, info) in enumerate(professors.items()):
        for course in info['courses']:
            if course in courses:
                course_index = courses.index(course)
                matrice_profesori[i][course_index] = 1

    print("\nMatricea de disponibilitate a profesorilor:")
    print(matrice_disponibilitate)

    print("\nMatricea de alocare a cursurilor către studenți:")
    print(matrice_grupe)

    print("\nMatricea de alocare a cursurilor către profesori:")
    print(matrice_profesori)


if __name__ == "__main__":
    main()
