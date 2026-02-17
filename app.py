import sqlite3
import tkinter as tk
from tkinter import ttk, Toplevel

# --- GUI Setup --- #
root = tk.Tk()
root.title("Noodle App")
root.geometry("380x300")
root.resizable(width=False,height=False)
notebook = ttk.Notebook(root)

light_mode_bg = "#F2F2F2"
light_mode_text = "000000"
dark_mode_bg = "#303030"
dark_mode_text = "#EBEBEB"

connection = sqlite3.connect("data.db")
conn = connection.cursor()
conn.execute("""CREATE TABLE IF NOT EXISTS noodles (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Method TEXT,
    Rating INTEGER)""")

def quit_app():
    root.quit()

# --- Settings --- #
def settings_menu():
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("240x200")
    settings_window.resizable(width=False, height=False)

    def change_theme():
        root_bg = root.cget("bg")
        if root_bg == dark_mode_bg:
            new_bg = light_mode_bg
        else:
            new_bg = dark_mode_bg
        root.configure(bg=new_bg)

    def delete_all():
        pass
        # conn.execute("DELETE * FROM noodles")
        if conn.rowcount == 0:
            pass
            # output.set("No noodle dishes exist yet!")

    def auto_populate():
        pass

    tk.Button(settings_window,text="Switch Light/Dark Mode",command=change_theme).pack(side=tk.TOP,expand=True,fill="both",padx=5,pady=5)
    tk.Button(settings_window,text="Delete All Noodle Dishes",command=delete_all).pack(side=tk.TOP,expand=True,fill="both",padx=5,pady=5)
    tk.Button(settings_window,text="Auto-populate List of Noodle Dishes",command=auto_populate).pack(side=tk.TOP,expand=True,fill="both",padx=5,pady=5)

tk.Button(root,text="Settings",command=settings_menu).pack(side=tk.BOTTOM,pady=5)

# --- Notebook Tabs --- #
# Tab 1: Add New
tab_1 = tk.Frame(notebook)
notebook.add(tab_1,text="Add New")

def add_noodle():
    try:
        name = name_entry.get("1.0",tk.END).strip().title()
        method = method_entry.get("1.0",tk.END).strip().title()
        if not name:
            add_output.set("Please enter a name!")
        elif not method:
            add_output.set("Please enter a method!")
        else:
            rating = int(rating_entry.get("1.0",tk.END).strip())
            conn.execute("INSERT INTO noodles (Name, Method, Rating) VALUES (?, ?, ?);", (name, method, rating))
            connection.commit()
            add_output.set(f"Successfully added {name}, {method}! ({rating}/10)")
    except ValueError:
        add_output.set("Please enter a valid integer rating!")

name_lbl = tk.Label(tab_1,text="Enter the name of the noodle dish: ")
name_lbl.grid(row=0,column=0,padx=5,pady=10,sticky="w")
name_entry = tk.Text(tab_1,width=18,height=1)
name_entry.grid(row=0,column=1,padx=5,pady=10)

method_lbl = tk.Label(tab_1,text="Enter how it was prepared: ")
method_lbl.grid(row=1,column=0,padx=5,pady=10,sticky="w")
method_entry = tk.Text(tab_1,width=18,height=1)
method_entry.grid(row=1,column=1,padx=5,pady=10)

rating_lbl = tk.Label(tab_1,text="Enter your integer rating score (0-10): ")
rating_lbl.grid(row=2,column=0,padx=5,pady=10,sticky="w")
rating_entry = tk.Text(tab_1,width=18,height=1)
rating_entry.grid(row=2,column=1,padx=5,pady=10)

tk.Button(tab_1,text="Add Noodle Dish",command=add_noodle).grid(row=3,padx=5,pady=10,sticky="w")

add_output = tk.StringVar()
add_output_lbl= tk.Label(tab_1,textvariable=add_output)
add_output_lbl.grid(row=4,padx=5,pady=10,sticky="w",columnspan=2)
add_output.set("")

# Tab 2: Delete
tab_2 = tk.Frame(notebook)
notebook.add(tab_2,text="Delete")

def delete_noodle():
    try:
        to_delete = to_delete_entry.get("1.0",tk.END).strip().title()
        if not to_delete:
            delete_output.set("Please enter a name!")
        else:
            delete_id = int(delete_id_entry.get("1.0",tk.END).strip())
            conn.execute("DELETE FROM noodles WHERE name = ? and ID = ?",(to_delete, delete_id))
            if conn.rowcount == 0:
                delete_output.set("Noodle dish not found!")
            else:
                connection.commit()
                delete_output.set(f"Successfully deleted {to_delete} (ID: {delete_id})!")
    except ValueError:
        delete_output.set("Please enter a valid ID!")

to_delete_lbl = tk.Label(tab_2,text="Enter the noodle dish to delete: ")
to_delete_lbl.grid(row=0,column=0,padx=5,pady=10,sticky="w")
to_delete_entry = tk.Text(tab_2,width=22,height=1)
to_delete_entry.grid(row=0,column=1,padx=5,pady=10,sticky="e")

delete_id_lbl = tk.Label(tab_2,text="Enter specific ID: ")
delete_id_lbl.grid(row=1,column=0,padx=5,pady=10,sticky="w")
delete_id_entry = tk.Text(tab_2,width=22,height=1)
delete_id_entry.grid(row=1,column=1,padx=5,pady=10,sticky="e")

tk.Button(tab_2,text="Delete Noodle Dish",command=delete_noodle).grid(row=2,padx=5,pady=10,sticky="w")

delete_output = tk.StringVar()
delete_output_lbl= tk.Label(tab_2,textvariable=delete_output)
delete_output_lbl.grid(row=3,padx=5,pady=10,sticky="w",columnspan=2)
delete_output.set("")

# Tab 3: See All Noodles
tab_3 = tk.Frame(notebook)
notebook.add(tab_3,text="See All Noodles")

def populate_table(existing_data):
    if existing_data:
        for data in noodle_table.get_children():
            noodle_table.delete(data)
    all_noodles = conn.execute("SELECT * FROM noodles;")
    for item in all_noodles:
        noodle_table.insert("","end",values=(item[0], item[1], item[2], item[3]))

def sort_noodle_table(sort_table, header, descending):
    sort_noodles = [(sort_table.set(data, header), data) for data in sort_table.get_children("")]
    sort_noodles.sort(reverse=descending)
    for index, (value, data) in enumerate(sort_noodles):
        sort_table.move(data, "", index)
    sort_table.heading(header,command=lambda: sort_noodle_table(sort_table,header,not descending))

sort_lbl = tk.Label(tab_3, text="Click column headers to sort!")
sort_lbl.grid(row=0,column=0,padx=5,pady=10,sticky="w")

columns = ("ID","Name","Method","Rating")
noodle_table = ttk.Treeview(tab_3, columns=columns, show="headings")
noodle_table.column(column="#0",stretch=False)
noodle_table.column(column="ID",width=30)
noodle_table.column(column="Name",width=175)
noodle_table.column(column="Method",width=100)
noodle_table.column(column="Rating",width=60)
noodle_table.grid(row=1,column=0,padx=5,columnspan=3)

for column in columns:
    noodle_table.heading(column,text=column,command=lambda col=column: sort_noodle_table(noodle_table, col, False))

tk.Button(tab_3,text="Refresh",command=lambda:populate_table(True)).grid(row=0,column=2,padx=5,pady=10,sticky="e")

notebook.pack(expand=True,fill="both")
populate_table(False)
root.mainloop()