import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import messagebox
import pyodbc



# Replace with your server name and database name
server = 'OMAR\SQLEXPRESS'
database = 'JobTracker'

# Replace with your username and password
username = 'omar'
password = 'omarelfeky01'

# Connect to the database
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

# Use the connection
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM JobApplications")

# Fetch the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection

jobs = []


def add_job():
    company = company_entry.get()
    position = position_entry.get()
    status = status_var.get()
    date_applied = date_entry.get()

    if not company or not position or not status or not date_applied:
        # Show an error message if any of the fields is empty
        messagebox.showerror("Error", "Please fill in all the fields.")
        return

    jobs.append({
        "company": company,
        "position": position,
        "status": status,
        "date_applied": date_applied
    })
    applied_date = datetime.datetime.now()
    formatted_date = applied_date.strftime("%Y-%m-%d")

    # Insert the job data into the database
    cursor.execute("INSERT INTO JobApplications (job_title, company_name, applied_date, status) VALUES (?, ?, ?, ?)", (position, company, date_applied, status))
    cnxn.commit()

    # Clear the input fields
    company_entry.delete(0, tk.END)
    position_entry.delete(0, tk.END)
    status_var.set("")
    date_entry.delete(0, tk.END)
    


def insert_date():
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




root = tk.Tk()
root.title("Job Tracker")

def select_job(event):
    selected_item = result_tree.focus()
    result_tree.item(selected_item, tags=("selected",))
    




tree = ttk.Treeview(root)
def delete_job():
    selected_item = result_tree.selection()
    if selected_item:
        result = messagebox.askyesno("Confirmation", "Are you sure you want to delete this entry?")
        if result:
            # Get the id of the selected item
            selected_item_id = result_tree.item(selected_item)['text']
            result_tree.delete(selected_item)
            cursor.execute("DELETE FROM JobApplications WHERE id = ?", (selected_item_id,))
            cnxn.commit()
    else:
        messagebox.showerror("Error", "Please select an entry to delete.")




# Create labels
company_label = tk.Label(root, text="Company:")
position_label = tk.Label(root, text="Position:")
status_label = tk.Label(root, text="Status:")
date_label = tk.Label(root, text="Date Applied:")

# Create entry fields
company_entry = tk.Entry(root)
position_entry = tk.Entry(root)
date_entry = tk.Entry(root)
result_text = tk.Text(root)

# Create a drop-down menu for the status field
status_var = tk.StringVar()
status_var.set("")
status_entry = ttk.Combobox

# Create a drop-down menu for the status field
status_var = tk.StringVar()
status_var.set("")
status_entry = ttk.Combobox(root, textvariable=status_var, values=["Applied", "Interviewed", "Offered", "Rejected"])





# Create the Treeview widget
result_tree = ttk.Treeview(root, columns=("Position", "Company", "Date Applied", "Status"), show='headings')
result_tree.heading("Company", text="Company")
result_tree.heading("Position", text="Position")
result_tree.heading("Status", text="Status")
result_tree.heading("Date Applied", text="Date Applied")
result_tree.column("#0", width=100, minwidth=100)
result_tree.column("#1", width=100, minwidth=100)
result_tree.column("#2", width=100, minwidth=100)
result_tree.column("#3", width=100, minwidth=100)
result_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

def view_jobs():
    result_tree.delete(*result_tree.get_children())
    cursor.execute("SELECT id, job_title, company_name, CAST(applied_date AS varchar(10)), status FROM JobApplications")
    rows = cursor.fetchall()
    for row in rows:
        result_tree.insert("", "end", values=row)






# Create buttons
add_button = tk.Button(root, text="Add Job", command=add_job)
view_button = tk.Button(root, text="View Jobs", command=view_jobs)
date_button = tk.Button(root, text="Insert Date", command=insert_date)
delete_button = tk.Button(root, text="Delete Job", command=delete_job)



# Position the widgets on the screen
company_label.grid(row=0, column=0)
position_label.grid(row=1, column=0)
status_label.grid(row=2, column=0)
date_label.grid(row=3, column=0)

company_entry.grid(row=0, column=1)
position_entry.grid(row=1, column=1)
status_entry.grid(row=2, column=1)
date_entry.grid(row=3, column=1)

add_button.grid(row=4, column=0)
view_button.grid(row=4, column=1)
date_button.grid(row=4, column=2)
delete_button.grid(row=4, column=3)


# Add the job information to the Treeview
for job in jobs:
    result_tree.insert('', 'end', values=(job['company'], job['position'], job['status'], job['date_applied']))

root.mainloop()
cursor.close()
cnxn.close()

