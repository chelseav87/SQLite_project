import database

MENU_PROMPT = """

--- Coffee Bean App ---

Please choose one of these options:

1) Add a new bean.
2) Find a bean by name.
3) See all beans.
4) Search beans by rating.
5) See which preparation method is best for a bean.
6) Delete bean by name.
7) Exit.

Your selection: """

def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "7":
        if user_input == "1":
            prompt_add_new_bean(connection)
        elif user_input == "2":
            prompt_find_bean(connection)
        elif user_input == "3":
            prompt_see_all_beans(connection)
        elif user_input == "4":
            prompt_search_bean_by_rating(connection)
        elif user_input == "5":
            prompt_find_best_method(connection)
        elif user_input == "6":
            prompt_delete_bean(connection)
        else:
            print("Invalid input, please try again!")

def prompt_add_new_bean(connection):
    name = input("Enter bean name: ").title()
    if not name:
        print("Please enter a name!")
        return
    method = input("Enter how you've prepared it: ").title()
    if not method:
        print("Please enter a method!")
        return
    rating = int(input("Enter your rating score (0-10): "))
    if rating < 0 or rating > 10:
        print("Invalid input, please try again!")
        return
    else:
        database.add_bean(connection, name, method, rating)
        print(f"Added {name}, {method}!")

def prompt_find_bean(connection):
    name = input("Enter bean name to find: ").title()
    beans = database.get_beans_by_name(connection, name)
    if not beans:
        print("Cannot find bean name!")
    else:
        for bean in beans:
            print(f"{bean[1]}, {bean[2]} | {bean[3]}/10")

def prompt_see_all_beans(connection):
    beans = database.get_all_beans(connection)
    if not beans:
        print("No beans found!")
    else:
        for bean in beans:
            print(f"{bean[1]}, {bean[2]} | {bean[3]}/10")

def prompt_search_bean_by_rating(connection):
    try:
        min_rating = int(input("Enter minimum range (0-10): "))
        max_rating = int(input("Enter maximum range (0-10): "))
        if min_rating < 0 or max_rating > 10 or min_rating > max_rating:
            print("Invalid range, please try again!")
            return
        else:
            beans = database.get_beans_by_rating(connection, min_rating, max_rating)
            if not beans:
                print("No beans within that range!")
            else:
                for bean in beans:
                    print(f"{bean[1]}, {bean[2]} | {bean[3]}/10")
    except ValueError:
        print("Invalid input, please try again!")


def prompt_find_best_method(connection):
    name = input("Enter bean name to find: ").title()
    try:
        best_method = database.get_best_preparation_for_bean(connection, name)
        print(f"The best preparation method for {name} is {best_method[2]}!")
    except TypeError:
        print("Cannot find bean name!")

def prompt_delete_bean(connection):
    name = input("Enter bean name to delete: ").title()
    beans = database.get_beans_by_name(connection, name)
    if not beans:
        print("Cannot find bean name!")
    else:
        for bean in beans:
            print(f"{bean[0]}: {bean[1]}, {bean[2]} | {bean[3]}/10")
        try:
            bean_id = int(input("\nEnter the ID of the bean you want to delete: "))
            valid_id = [bean[0] for bean in beans]
            if bean_id not in valid_id:
                print("Invalid ID, please try again!")
            else:
                database.delete_bean(connection, name, bean_id)
                print(f"ID {bean_id}: {name} deleted!")
        except ValueError:
            print("Invalid input, please try again!")

menu()