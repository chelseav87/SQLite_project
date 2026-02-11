import database
import tkinter as tk
from tkinter import ttk

### --- GUI Setup --- ###
root = tk.Tk()
root.title("Noodle App")
root.geometry("400x380")
root.resizable(False, False)
notebook = ttk.Notebook(root)
notebook.pack(expand=True)

### --- Menu Functions --- ###
user_input_error = "Invalid input, please try again!"

def menu():
    connection = database.connect()
    database.create_tables(connection)


def prompt_find_noodle(connection):
    name = input("Enter noodle dish to find: ").title()
    noodles = database.get_noodles_by_name(connection, name)
    if not noodles:
        print("Cannot find noodle dish!")
    else:
        for noodle in noodles:
            print(f"{noodle[1]}, {noodle[2]} | {noodle[3]}/10")

def prompt_see_all_noodles(connection):
    noodles = database.get_all_noodles(connection)
    if not noodles:
        print("No noodle dishes found!")
    else:
        for noodle in noodles:
            print(f"{noodle[1]}, {noodle[2]} | {noodle[3]}/10")

def prompt_search_noodle_by_rating(connection):
    try:
        min_rating = int(input("Enter minimum range (0-10): "))
        max_rating = int(input("Enter maximum range (0-10): "))
        if min_rating < 0 or max_rating > 10 or min_rating > max_rating:
            print(user_input_error)
            return
        else:
            noodles = database.get_noodles_by_rating(connection, min_rating, max_rating)
            if not noodles:
                print("No noodle dishes within that range!")
            else:
                for noodle in noodles:
                    print(f"{noodle[1]}, {noodle[2]} | {noodle[3]}/10")
    except ValueError:
        print(user_input_error)

def prompt_find_best_method(connection):
    name = input("Enter noodle dish to find: ").title()
    try:
        best_method = database.get_best_preparation_for_noodle(connection, name)
        print(f"The best preparation method for {name} is {best_method[2]}!")
    except TypeError:
        print("Cannot find noodle dish!")

def prompt_delete_noodle(connection):
    name = input("Enter noodle dish to delete: ").title()
    noodles = database.get_noodles_by_name(connection, name)
    if not noodles:
        print("Cannot find noodle dish!")
    else:
        for noodle in noodles:
            print(f"{noodle[0]}: {noodle[1]}, {noodle[2]} | {noodle[3]}/10")
        try:
            noodle_id = int(input("\nEnter the ID of the noodle dish you want to delete: "))
            valid_id = [noodle[0] for noodle in noodles]
            if noodle_id not in valid_id:
                print(user_input_error)
            else:
                database.delete_noodle(connection, name, noodle_id)
                print(f"ID {noodle_id}: {name} deleted!")
        except ValueError:
            print(user_input_error)

def quit_app():
    root.quit()

### --- Notebook Tabs --- ###
tab_add = ttk.Frame(notebook)
notebook.add(tab_add,text="Add New Noodle Dish")

    name_label = ttk.Label(tab_add,text="Enter the name of the noodle dish: ")
    name_label.pack(pady=5)
    name_input = ttk.Entry(tab_add)
    name_input.pack(pady=5)

method_label = ttk.Label(tab_add,text="Enter how it was prepared: ")
method_label.pack(pady=5)
method_input = ttk.Entry(tab_add)
method_input.pack(pady=5)

rating_label = ttk.Label(tab_add,text="Enter your integer rating score (0-10): ")
rating_label.pack(pady=5)
rating_input = ttk.Entry(tab_add)
rating_input.pack(pady=5)

def prompt_add_new_noodle(name, method, rating):
    try:
        name = name_label

        print(f"Added {name}, {method}!")
    except ValueError

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

tab_delete = ttk.Frame(notebook)
notebook.add(tab_delete,text="Delete Noodle Dish")

tab_all = ttk.Frame(notebook)
notebook.add(tab_all,text="See All Noodle Dishes")


tk.Button(root, text="Exit.", command=quit_app).pack(pady=5)

root.mainloop()