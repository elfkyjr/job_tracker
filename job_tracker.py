import tkinter as tk
from tkinter import ttk
import os
import sys
import subprocess

class JobTracker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Job Tracker")
        self.geometry("300x450")

        self.job_list = ttk.Treeview(self)
        self.job_list["columns"] = ("Title","Company", "Status")
        self.job_list.heading("Title", text="Title")
        self.job_list.heading("Company", text="Company")
        self.job_list.heading("Status", text="Status")
        self.job_list.pack()
        self.job_list.bind("<Double-1>", self.delete_job)

        self.add_job_frame = ttk.Frame(self)
        self.add_job_frame.pack()

        self.title_label = ttk.Label(self.add_job_frame, text="Title:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5)

        self.title_entry = ttk.Entry(self.add_job_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.company_label = ttk.Label(self.add_job_frame, text="Company:")
        self.company_label.grid(row=1, column=0, padx=5, pady=5)

        self.company_entry = ttk.Entry(self.add_job_frame)
        self.company_entry.grid(row=1, column=1, padx=5, pady=5)

        self.status_label = ttk.Label(self.add_job_frame, text="Status:")
        self.status_label.grid(row=2, column=0, padx=5, pady=5)

        self.status_var = tk.StringVar()
        self.status_var.set("Applied")
        self.status_dropdown = ttk.OptionMenu(self.add_job_frame, self.status_var, "Applied", "First Interview", "Ghosted", "Rejected", "Accepted")
        self.status_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.add_job_button = ttk.Button(self.add_job_frame, text="Add Job", command=self.add_job)
        self.add_job_button.grid(row=3, column=1, padx=5, pady=5)

    def add_job(self):
        title = self.title_entry.get()
        company = self.company_entry.get()
        status = self.status_var.get()
        self.job_list.insert("", "end", text="", values=(title, company, status))

    def delete_job(self, event):
        selected_job = self.job_
