import database

user_input_error = "Invalid input, please try again!"

MENU_PROMPT = """

--- Noodle App ---

Please choose one of these options:

1) Add a new noodle dish.
2) Find a noodle dish by name.
3) See all noodle dishes.
4) Search noodle dishes by rating.
5) See which preparation method is best for a noodle dish.
6) Delete a noodle dish by name.
7) Exit.

Your selection: """

def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "7":
        if user_input == "1":
            prompt_add_new_noodle(connection)
        elif user_input == "2":
            prompt_find_noodle(connection)
        elif user_input == "3":
            prompt_see_all_noodles(connection)
        elif user_input == "4":
            prompt_search_noodle_by_rating(connection)
        elif user_input == "5":
            prompt_find_best_method(connection)
        elif user_input == "6":
            prompt_delete_noodle(connection)
        else:
            print(user_input_error)

def prompt_add_new_noodle(connection):
    name = input("Enter the name of the noodle dish: ").title()
    if not name:
        print(user_input_error)
        return
    method = input("Enter how it was prepared: ").title()
    if not method:
        print(user_input_error)
        return
    rating = int(input("Enter your integer rating score (0-10): "))
    if rating < 0 or rating > 10:
        print(user_input_error)
        return
    else:
        database.add_noodle(connection, name, method, rating)
        print(f"Added {name}, {method}!")

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

menu()