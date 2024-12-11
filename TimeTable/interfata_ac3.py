import tkinter as tk
from tkinter import messagebox, scrolledtext
from ac3 import main
import numpy as np
from collections import deque
from read_f_file import read_file_timetable
from read_f_prompt import read_prompt_timetable
from ac3 import run_main_from_gui


# Funcție pentru a înlocui apelul main() cu interfața grafică
def run_with_gui():
    # Creăm fereastra principală
    root = tk.Tk()
    root.title("Interfață AC3 - Planificare cursuri")

    # Setăm dimensiunea ferestrei
    root.geometry("600x400")

    # Etichetă pentru titlu
    title_label = tk.Label(root, text="Planificare Cursuri - AC3", font=("Arial", 16))
    title_label.pack(pady=10)

    # Meniu de selecție pentru alegerea metodei de citire a datelor
    def on_select_method():
        choice = method_var.get()
        result = ""

        if choice == "1":
            # Read data from the prompt
            courses, professors, classrooms, groups, constraints, week_days, time_slots = read_prompt_timetable()
            result = run_main_from_gui("1")  # Call main using choice 1

        elif choice == "2":
            # Read data from file
            file_name = file_name_entry.get()  # Get the file name entered by the user
            if file_name:
                courses, professors, classrooms, groups, constraints, week_days, time_slots = read_file_timetable(
                    file_name)
                result = run_main_from_gui("2", file_name)  # Call main using choice 2
            else:
                messagebox.showwarning("Warning", "Te rog să introduci un nume de fișier.")
                return  # Exit if the file name is not provided

        else:
            messagebox.showerror("Error", "Opțiune invalidă!")  # Handle invalid choice
            return

        # Display the result in the text box
        text_box.delete(1.0, tk.END)  # Clear the existing content
        text_box.insert(tk.END, result)  # Insert the new content

    # Etichetă pentru a explica selecția
    method_label = tk.Label(root, text="Alege metoda de citire a datelor:")
    method_label.pack(pady=5)

    # Variabilă pentru a păstra selecția utilizatorului
    method_var = tk.StringVar(value="1")

    # Creăm un meniu radio pentru citirea din prompt sau fișier
    prompt_radio = tk.Radiobutton(root, text="Citire prompt", variable=method_var, value="1")
    prompt_radio.pack()

    file_radio = tk.Radiobutton(root, text="Citire fișier", variable=method_var, value="2")
    file_radio.pack()

    # Căsuță de text pentru numele fișierului (dacă este ales citirea din fișier)
    file_name_label = tk.Label(root, text="Introduceti numele fișierului:")
    file_name_label.pack(pady=5)

    file_name_entry = tk.Entry(root, width=40)
    file_name_entry.pack(pady=5)

    # Buton pentru a lansa citirea datelor
    read_button = tk.Button(root, text="Începe citirea", command=on_select_method)
    read_button.pack(pady=20)

    # Text box cu derulare pentru a vizualiza domeniile
    text_box = scrolledtext.ScrolledText(root, width=70, height=15)
    text_box.pack(padx=10, pady=10)

    # Funcție pentru a afișa domeniile în text box
    def display_domains(csp, zile, intervale, classrooms):
        text_box.delete(1.0, tk.END)  # Curăță textul existent

        for course, domain in csp['domains'].items():
            text_box.insert(tk.END, f"Domain of {course}:\n")
            formatted_domain = format_domain(domain, zile, intervale, classrooms)
            for entry in formatted_domain:
                text_box.insert(tk.END, f"  - {entry}\n")
            text_box.insert(tk.END, "\n")  # Linie goală după fiecare curs

    # Funcție de formatare a domeniilor
    def format_domain(domain, zile, intervale, classrooms):
        formatted_domain = []
        for day_idx, time_idx, room_idx in domain:
            day = zile[day_idx]
            time = intervale[time_idx]
            room = classrooms[room_idx]
            formatted_domain.append(f"{day} {time} (Room {room})")
        return formatted_domain


