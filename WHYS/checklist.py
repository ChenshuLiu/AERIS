import tkinter as tk
from tkinter import messagebox
import json
import os

class ChecklistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checklist App")

        self.file_path = "tasks.json" # storing the check list file
        '''
        Store the following information:
        - List of items
        - Meta-data of the items
            - Complete/Incomplete
            - Deleted
        '''

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # instantiate the chatbox
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=5)

        # instantiate the buttons
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        # instantiate the list display box
        self.listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.MULTIPLE) # the box that displays all the entry elements
        self.listbox.pack(pady=10)

        self.complete_button = tk.Button(root, text="Mark Completed", command=self.complete_task)
        self.complete_button.pack()

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.load_tasks()  # Load tasks when the app starts, initialize the history using __init__ constructor

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.listbox.insert(tk.END, task) # insert the new entry from the task box to the END of the list
            self.task_entry.delete(0, tk.END) # after appending the new entry, refresh the task entry box for new entries
            self.save_tasks()  # Save after adding a new task

    def complete_task(self):
        selected_items = self.listbox.curselection() # cursor defines the indices of the items selected from the list
        for index in selected_items:
            self.listbox.itemconfig(index, {'bg': 'lightgrey'}) # all items selected will be marked into grey
        self.save_tasks()  # Save completed tasks

    def delete_task(self):
        selected_items = list(self.listbox.curselection())[::-1]  # Reverse to avoid shifting indexes
        for index in selected_items:
            self.listbox.delete(index)
        self.save_tasks()  # Save after deletion

    def save_tasks(self):
        tasks = self.listbox.get(0, tk.END)  # Get all tasks (start from 0, all the way to the end of the list)
        with open(self.file_path, "w") as file:
            json.dump(tasks, file)  # Save as JSON

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    tasks = json.load(file)
                    for task in tasks:
                        self.listbox.insert(tk.END, task) # iteratively insert items stored in the checklist to the list (to each END of the list)
                except json.JSONDecodeError:
                    pass  # If the file is empty or corrupted, do nothing

if __name__ == "__main__":
    root = tk.Tk()
    app = ChecklistApp(root)
    root.mainloop()
