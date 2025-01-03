import tkinter as tk
import re
from tkinter import filedialog, messagebox
import numpy as np  # Asigură-te că numpy este importat
from timetable import run_scheduler
from read_f_file import read_file_timetable
from read_f_prompt import read_prompt_timetable
from interfata_ac3 import run_with_gui


# Funcția care va genera orarul pentru fiecare sală într-o fereastră separată
def display_schedule_window_per_room(schedule, week_days, time_slots, classrooms):
    main_window = tk.Toplevel()
    main_window.title("Alege sala pentru a vizualiza orarul")
    main_window.geometry("400x400")

    def show_room_schedule(room_idx):
        classroom = classrooms[room_idx]
        schedule_window = tk.Toplevel()
        schedule_window.title(f"Orar pentru {classroom}")

        # Adaugă zilele săptămânii pe prima linie
        for col, day in enumerate(week_days):
            label = tk.Label(schedule_window, text=day, relief="solid", width=20, height=2, font=('Arial', 12))
            label.grid(row=0, column=col + 1)

        # Adaugă intervalele orare pe prima coloană
        for row, time in enumerate(time_slots):
            label = tk.Label(schedule_window, text=time, relief="solid", width=20, height=2, font=('Arial', 12))
            label.grid(row=row + 1, column=0)

        # Umple celulele orarului pentru sala selectată
        for day_idx, day in enumerate(week_days):
            for time_idx, time in enumerate(time_slots):
                event = schedule[day_idx][time_idx][room_idx]  # Accessing the 3D timetable matrix
                if event:  # If there's an event, display it
                    label = tk.Label(schedule_window, text=event, relief="solid", width=20, height=2, bg="lightgreen",
                                     font=('Arial', 12))
                    label.grid(row=time_idx + 1, column=day_idx + 1)
                else:  # If there's no event, show a placeholder
                    label = tk.Label(schedule_window, text="-", relief="solid", width=20, height=2, font=('Arial', 12))
                    label.grid(row=time_idx + 1, column=day_idx + 1)

    # Creează un meniu pentru fiecare sală
    for idx, room in enumerate(classrooms):
        button = tk.Button(main_window, text=f"Vezi orarul pentru {room}",
                           command=lambda index=idx: show_room_schedule(index), font=('Arial', 14))
        button.pack(pady=10)


def extract_professor(event_string):
    start_idx = event_string.rfind('(') + 1
    end_idx = event_string.rfind(')')
    if start_idx != -1 and end_idx != -1:
        return event_string[start_idx:end_idx].strip()
    return ""  # În caz că nu găsim profesorul


# Funcția care va genera orarul pentru profesori într-o fereastră separată
def display_schedule_window_per_teacher(schedule, week_days, time_slots, professors, classrooms):
    main_window = tk.Toplevel()
    main_window.title("Alege profesorul pentru a vizualiza orarul")
    main_window.geometry("400x400")

    # Funcție care creează fereastra cu orarul pentru un profesor specific
    def show_teacher_schedule(teacher_index):
        teacherr = professors[teacher_index]  # Aici accesezi profesorul din lista direct
        schedule_window = tk.Toplevel()
        schedule_window.title(f"Orar pentru {teacherr}")

        # Adaugă zilele săptămânii pe prima linie
        for col, day in enumerate(week_days):
            label = tk.Label(schedule_window, text=day, relief="solid", width=20, height=2, font=('Arial', 12))
            label.grid(row=0, column=col + 1)  # +1 pentru a lăsa colțul liber pentru intervalele orare

        # Adaugă intervalele orare pe prima coloană
        for row, time in enumerate(time_slots):
            label = tk.Label(schedule_window, text=time, relief="solid", width=20, height=2, font=('Arial', 12))
            label.grid(row=row + 1, column=0)  # +1 pentru a lăsa linia liberă pentru zile

        # Umple celulele orarului pentru profesorul selectat
        for day_idx, day in enumerate(week_days):
            for time_idx, time in enumerate(time_slots):
                events = schedule[day_idx][time_idx]  # Acum este o listă de evenimente
                if events:  # Dacă există evenimente pentru acea perioadă
                    for event in events:
                        professor_in_event = extract_professor(event)
                        if professor_in_event == teacherr:  # Verifică dacă profesorul corespunde
                            # Află indexul sălii
                            room_idx = events.index(event)
                            room = classrooms[room_idx]  # Sala este obținută din lista classrooms

                            # Extrage doar informațiile relevante despre curs (fără (A) - A redundante)
                            event_string = re.sub(r'(\([^)]*\))[^)]*$', '', event)

                            # Afișează doar cursul și sala, fără redundanță
                            label = tk.Label(schedule_window, text=f"{event_string} {room}", relief="solid", width=20,
                                             height=2, bg="lightgreen", font=('Arial', 12))
                            label.grid(row=time_idx + 1, column=day_idx + 1)
                else:  # Dacă nu există niciun eveniment, lasă celula goală
                    label = tk.Label(schedule_window, text="-", relief="solid", width=20, height=2, font=('Arial', 12))
                    label.grid(row=time_idx + 1, column=day_idx + 1)

    # Creează un buton pentru fiecare profesor
    for teacher_idx, teacher in enumerate(professors):  # Folosește `professors` direct (ca listă)
        button = tk.Button(main_window, text=f"Vezi orarul pentru {teacher}",
                           command=lambda teacher_index=teacher_idx: show_teacher_schedule(teacher_index),
                           font=('Arial', 14))
        button.pack(pady=5)


# Funcția care va fi apelată la submit pentru a procesa datele
def on_submit():
    choice = method_var.get()

    if choice == 1:
        courses, professors, classrooms, groups, constraints, week_days, time_slots = read_prompt_timetable()
        timetable = [[["" for _ in classrooms] for _ in time_slots] for _ in week_days]
        professor_indices = {prof: i for i, prof in enumerate(professors.keys())}
        availability = np.zeros((len(week_days), len(time_slots), len(professors)), dtype=int)
        preferences = {}

        # Rulează schedulerul
        schedule = run_scheduler(courses, professors, classrooms, constraints, week_days, time_slots, timetable,
                                 professor_indices, availability, preferences)
    elif choice == 2:
        file_name = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_name:
            courses, professors, classrooms, groups, constraints, week_days, time_slots = read_file_timetable(file_name)
            timetable = [[["" for _ in classrooms] for _ in time_slots] for _ in week_days]
            professor_indices = {prof: i for i, prof in enumerate(professors.keys())}
            availability = np.zeros((len(week_days), len(time_slots), len(professors)), dtype=int)
            preferences = {}

            # Rulează schedulerul
            schedule = run_scheduler(courses, professors, classrooms, constraints, week_days, time_slots, timetable,
                                     professor_indices, availability, preferences)
        else:
            schedule = "Nu s-a selectat un fisier."
    else:
        schedule = "Opțiune invalida!"

    # Afișează o fereastră care întreabă dacă vrei să vezi orarul pentru sali sau profesori
    choice_window = tk.Toplevel()
    choice_window.title("Alege opțiunea")
    choice_window.geometry("400x400")

    def show_room_schedule():
        display_schedule_window_per_room(schedule, week_days, time_slots, classrooms)

    def show_teacher_schedule():
        display_schedule_window_per_teacher(schedule, week_days, time_slots, list(professors.keys()), classrooms)

    # Butoane pentru alegerea între sală și profesor
    title_label1 = tk.Label(choice_window, text="Vezi orarul pentru", font=("Arial", 22))
    title_label1.pack(pady=10)
    room_button = tk.Button(choice_window, text="săli", command=show_room_schedule,
                            font=('Arial', 16))
    room_button.pack(pady=10)

    teacher_button = tk.Button(choice_window, text="profesori", command=show_teacher_schedule,
                               font=('Arial', 16))
    teacher_button.pack(pady=10)

    # Buton pentru detalii
    title_label1 = tk.Label(choice_window, text="Sau vezi detalii", font=("Arial", 16))
    title_label1.pack(pady=50)
    details_button = tk.Button(choice_window, text="Detalii", command=...,
                               font=('Arial', 16))
    details_button.pack(pady=10)


def show_options():
    # Afișează opțiunile în aceeași fereastră
    back_button.place(x=0, y=0, width=25, height=25)
    options_label.pack(pady=30)
    prompt_radio.pack(anchor=tk.W)
    file_radio.pack(anchor=tk.W)
    start_button.pack(pady=20)
    submit_button.pack_forget()  # Ascunde butonul „Generează Orar”
    ac3_button.pack_forget()
    title_label.pack_forget()


def principal_gui():
    back_button.place_forget()
    options_label.pack_forget()
    prompt_radio.pack_forget()
    file_radio.pack_forget()
    start_button.pack_forget()
    title_label.pack(pady=30)
    submit_button.pack(pady=20)
    ac3_button.pack(pady=0)


# Interfața principală
root = tk.Tk()
root.title("Timetable Scheduler")
root.geometry("400x400")

method_var = tk.IntVar()

title_label = tk.Label(root, text="Timetable Scheduler", font=("Arial", 22))
title_label.pack(pady=30)

# Elemente pentru opțiuni
back_button = tk.Button(root, text="<", command=principal_gui, font=('Arial', 14))
options_label = tk.Label(root, text="Selectează metoda de citire:", font=("Arial", 18))
prompt_radio = tk.Radiobutton(root, text="Citire Prompt", variable=method_var, value=1, font=('Arial', 14))
file_radio = tk.Radiobutton(root, text="Citire Fișier", variable=method_var, value=2, font=('Arial', 14))
start_button = tk.Button(root, text="Start", command=on_submit, font=('Arial', 18))

# Butonul pentru generare orar
submit_button = tk.Button(root, text="Generează Orar", command=show_options, font=('Arial', 18))
submit_button.pack(pady=20)

# Butonul pentru afișarea de detalii
ac3_button = tk.Button(root, text="AC3", command=run_with_gui, font=('Arial', 18))
ac3_button.pack(pady=0)

root.mainloop()
