# https://pythonguides.com/python-tkinter-notebook/

import sqlite3
import tkinter as tk
from tkinter import ttk

# --- GUI Setup --- #
root = tk.Tk()
root.title("Noodle App")
root.geometry("380x410")
root.resizable(width=False,height=False)
notebook = ttk.Notebook(root)

# --- Menu Functions --- #
connection = sqlite3.connect("data.db")
conn = connection.cursor()
conn.execute("""CREATE TABLE IF NOT EXISTS noodles (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Method TEXT,
    Rating INTEGER)""")
user_input_error = "Invalid input, please try again!"

# def prompt_add_new_noodle(connection):
#     name = input("Enter the name of the noodle dish: ").title()
#     if not name:
#         print(user_input_error)
#         return
#     method = input("Enter how it was prepared: ").title()
#     if not method:
#         print(user_input_error)
#         return
#     rating = int(input("Enter your integer rating score (0-10): "))
#     if rating < 0 or rating > 10:
#         print(user_input_error)
#         return
#     else:
#         database.add_noodle(connection, name, method, rating)
#         print(f"Added {name}, {method}!")
#
# def prompt_find_noodle(connection):
#     name = input("Enter noodle dish to find: ").title()
#     noodles = database.get_noodles_by_name(connection, name)
#     if not noodles:
#         print("Cannot find noodle dish!")
#     else:
#         for noodle in noodles:
#             print(f"{noodle[1]}, {noodle[2]} | {noodle[3]}/10")
#
# def prompt_see_all_noodles(connection):
#     noodles = database.get_all_noodles(connection)
#     if not noodles:
#         print("No noodle dishes found!")
#     else:
#         for noodle in noodles:
#             print(f"{noodle[1]}, {noodle[2]} | {noodle[3]}/10")
#
# def prompt_search_noodle_by_rating(connection):
#     try:
#         min_rating = int(input("Enter minimum range (0-10): "))
#         max_rating = int(input("Enter maximum range (0-10): "))
#         if min_rating < 0 or max_rating > 10 or min_rating > max_rating:
#             print(user_input_error)
#             return
#         else:
#             noodles = database.get_noodles_by_rating(connection, min_rating, max_rating)
#             if not noodles:
#                 print("No noodle dishes within that range!")
#             else:
#                 for noodle in noodles:
#                     print(f"{noodle[1]}, {noodle[2]} | {noodle[3]}/10")
#     except ValueError:
#         print(user_input_error)
#
# def prompt_find_best_method(connection):
#     name = input("Enter noodle dish to find: ").title()
#     try:
#         best_method = database.get_best_preparation_for_noodle(connection, name)
#         print(f"The best preparation method for {name} is {best_method[2]}!")
#     except TypeError:
#         print("Cannot find noodle dish!")
#
# def prompt_delete_noodle(connection):
#     name = input("Enter noodle dish to delete: ").title()
#     noodles = database.get_noodles_by_name(connection, name)
#     if not noodles:
#         print("Cannot find noodle dish!")
#     else:
#         for noodle in noodles:
#             print(f"{noodle[0]}: {noodle[1]}, {noodle[2]} | {noodle[3]}/10")
#         try:
#             noodle_id = int(input("\nEnter the ID of the noodle dish you want to delete: "))
#             valid_id = [noodle[0] for noodle in noodles]
#             if noodle_id not in valid_id:
#                 print(user_input_error)
#             else:
#                 database.delete_noodle(connection, name, noodle_id)
#                 print(f"ID {noodle_id}: {name} deleted!")
#         except ValueError:
#             print(user_input_error)

def add_data():
    try:
        name = name_entry.get("1.0",tk.END).strip().title()
        method = method_entry.get("1.0",tk.END).strip().title()
        rating = int(rating_entry.get("1.0",tk.END).strip())
        conn.execute("INSERT INTO noodles (Name, Method, Rating) VALUES (?, ?, ?);", (name, method, rating))
        connection.commit()
        output.set(f"Added {name}, {method}! ({rating}/10)")
        conn.close()
    except ValueError:
        output.set(user_input_error)

def egg():
    pass

def quit_app():
    root.quit()

# --- Notebook Tabs --- #

# Tab 1: Add New
tab_1 = tk.Frame(notebook)
notebook.add(tab_1, text="Add New")

name_lbl = tk.Label(tab_1, text="Enter the name of the noodle dish: ")
name_lbl.grid(row=0,column=0,padx=5,pady=10,sticky="w")
name_entry = tk.Text(tab_1,width=18,height=1)
name_entry.grid(row=0,column=1,padx=5,pady=10)

method_lbl = tk.Label(tab_1, text="Enter how it was prepared: ")
method_lbl.grid(row=1,column=0,padx=5,pady=10,sticky="w")
method_entry = tk.Text(tab_1,width=18,height=1)
method_entry.grid(row=1,column=1,padx=5,pady=10)

rating_lbl = tk.Label(tab_1, text="Enter your integer rating score (0-10): ")
rating_lbl.grid(row=2,column=0,padx=5,pady=10,sticky="w")
rating_entry = tk.Text(tab_1,width=18,height=1)
rating_entry.grid(row=2,column=1,padx=5,pady=10)

tk.Button(tab_1, text="Add Noodle Dish", command=add_data).grid(row=3,padx=5,pady=5,sticky="w")
output = tk.StringVar()
output_lbl= tk.Label(tab_1, textvariable=output)
output_lbl.grid(row=4,padx=5,pady=5,sticky="w")
output.set("...")

# Tab 2: Delete
tab_2 = tk.Frame(notebook)
notebook.add(tab_2,text="Delete")

name1_lbl = tk.Label(tab_2, text="Enter the name of the noodle dish: ")
name1_lbl.grid(row=0,column=0,padx=5,pady=10,sticky="w")
name1_entry = tk.Text(tab_2,width=15,height=1)
name1_entry.grid(row=0,column=1,padx=5,pady=10)

noodle_table = ttk.Treeview(tab_2)
noodle_table["columns"]=("ID","Method","Rating")
noodle_table.column(column="#0",width=10)
noodle_table.column(column="ID",width=50)
noodle_table.column(column="Method",width=150)
noodle_table.column(column="Rating",width=150)
noodle_table.heading("ID",text="ID")
noodle_table.heading("Method",text="Method")
noodle_table.heading("Rating",text="Rating")
noodle_table.grid(row=2,column=0,padx=5,pady=0,sticky="w",columnspan=2)

id_lbl = tk.Label(tab_2, text="Enter the ID of the noodle dish to delete: ")
id_lbl.grid(row=4,column=0,padx=5,pady=10,sticky="w")
lbl_entry = tk.Text(tab_2,width=15,height=1)
lbl_entry.grid(row=4,column=1,padx=5,pady=10)

tk.Button(tab_2, text="< Prev", command=egg).grid(row=3,column=0,padx=5,pady=5,sticky="w")
tk.Button(tab_2, text="Next >", command=egg).grid(row=3,columnspan=2,column=0,padx=5,pady=5,sticky="e")
tk.Button(tab_2, text="Delete Noodle Dish", command=egg).grid(row=5,padx=5,pady=5,sticky="w")

# Tab 3: All Noodle Dishes
tab_3 = tk.Frame(notebook)
notebook.add(tab_3,text="All Noodle Dishes")

noodle_table = ttk.Treeview(tab_3)
noodle_table["columns"]=("ID","Name","Method","Rating")
noodle_table.column(column="#0",width=10)
noodle_table.column(column="ID",width=50)
noodle_table.column(column="Name",width=130)
noodle_table.column(column="Method",width=120)
noodle_table.column(column="Rating",width=50)
noodle_table.heading("ID",text="ID")
noodle_table.heading("Name",text="Name")
noodle_table.heading("Method",text="Method")
noodle_table.heading("Rating",text="Rating")
noodle_table.pack(fill="both",expand=True)

notebook.pack(expand=True,fill="both")

root.mainloop()