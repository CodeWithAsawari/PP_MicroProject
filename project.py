from tkinter import *
from tkinter import messagebox
import json


class StudyTask:

    def __init__(self, subject, homework, level, completed=False):
        self.subject = subject
        self.homework = homework
        self.level = level
        self.completed = completed

    def to_dict(self):
        return {
            "subject": self.subject,
            "homework": self.homework,
            "level": self.level,
            "completed": self.completed
        }


root = Tk()

root.title("Personal Study Organizer")
root.geometry("900x700")
root.config(bg="#e6f2ff")

tasks = []

def save_tasks():

    data = []

    for task in tasks:
        data.append(task.to_dict())

    with open("tasks.json", "w") as file:
        json.dump(data, file)


def load_tasks():

    global tasks

    try:
        with open("tasks.json", "r") as file:

            data = json.load(file)

            for item in data:

                task = StudyTask(
                    item["subject"],
                    item["homework"],
                    item["level"],
                    item["completed"]
                )

                tasks.append(task)

        refresh_list()

    except:
        pass

def refresh_list():

    task_listbox.delete(0, END)

    for task in tasks:

        mark = "✓" if task.completed else "*"

        text = f"{mark} {task.subject} - {task.homework} ({task.level})"

        task_listbox.insert(END, text)

def add_task():

    subj = subject.get().strip()
    hw = homework.get().strip()

    if not subj or not hw:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    new_task = StudyTask(
        subj,
        hw,
        level.get()
    )

    tasks.append(new_task)

    save_tasks()
    refresh_list()

    subject.delete(0, END)
    homework.delete(0, END)

def mark_completed():

    sel = task_listbox.curselection()

    if not sel:
        return

    tasks[sel[0]].completed = True

    save_tasks()
    refresh_list()

def delete_task():

    sel = task_listbox.curselection()

    if not sel:
        return

    del tasks[sel[0]]

    save_tasks()
    refresh_list()

header = Frame(root, bg="#003366", height=60)
header.pack(fill=X)

Label(
    header,
    text="📘 Personal Study Organizer 📘",
    font=("Comic Sans MS", 18, "bold"),
    fg="white",
    bg="#003366"
).pack(pady=10)

container = Frame(root, bg="#e6f2ff")
container.pack(fill=BOTH, expand=True, padx=15, pady=15)


input_frame = LabelFrame(
    container,
    text="📝 Add New Task",
    font=("Verdana", 12, "bold"),
    bg="#e6f2ff",
    fg="#003366",
    padx=10,
    pady=10
)

input_frame.pack(fill=X, pady=15)


Label(
    input_frame,
    text="Subject:",
    font=("Verdana", 11),
    bg="#e6f2ff"
).grid(row=0, column=0, pady=5)

subject = Entry(input_frame, width=30, font=("Verdana", 11))
subject.grid(row=0, column=1, padx=10)


Label(
    input_frame,
    text="Homework:",
    font=("Verdana", 11),
    bg="#e6f2ff"
).grid(row=1, column=0, pady=5)

homework = Entry(input_frame, width=30, font=("Verdana", 11))
homework.grid(row=1, column=1, padx=10)


Label(
    input_frame,
    text="Difficulty:",
    font=("Verdana", 11),
    bg="#e6f2ff"
).grid(row=2, column=0, pady=5)

level = StringVar(value="Easy")

level_frame = Frame(input_frame, bg="#e6f2ff")
level_frame.grid(row=2, column=1)

for opt in ["Easy", "Medium", "Hard"]:

    Radiobutton(
        level_frame,
        text=opt,
        variable=level,
        value=opt,
        bg="#e6f2ff"
    ).pack(side=LEFT)


list_frame = LabelFrame(
    container,
    text="📋 Your Tasks",
    font=("Verdana", 12, "bold"),
    bg="#e6f2ff",
    fg="#003366"
)

list_frame.pack(fill=BOTH, expand=True, pady=15)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=RIGHT, fill=Y)

task_listbox = Listbox(
    list_frame,
    font=("Verdana", 11),
    bg="white",
    fg="#003366",
    yscrollcommand=scrollbar.set
)

task_listbox.pack(fill=BOTH, expand=True)

scrollbar.config(command=task_listbox.yview)


button_frame = Frame(container, bg="#e6f2ff")
button_frame.pack(pady=10)

Button(
    button_frame,
    text="➕ Add Task",
    command=add_task,
    bg="#003366",
    fg="white",
    font=("Verdana", 11, "bold"),
    width=15
).pack(side=LEFT, padx=5)

Button(
    button_frame,
    text="✓ Completed",
    command=mark_completed,
    bg="#339966",
    fg="white",
    font=("Verdana", 11, "bold"),
    width=15
).pack(side=LEFT, padx=5)

Button(
    button_frame,
    text="🗑 Delete",
    command=delete_task,
    bg="#cc0000",
    fg="white",
    font=("Verdana", 11, "bold"),
    width=15
).pack(side=LEFT, padx=5)


load_tasks()


root.mainloop()
