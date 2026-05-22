# expense-tracker 
import json
import os
from pathlib import Path

# entry structure:
#   id, date, description, amount
#   id: unique int NOT NULL
#   date: month-day-year DEFAULT NOW()
#   description: string NOT NULL
#   amount: unsigned int NOT NULL

# allowed operations
#   add expenses --> expense-tracker add --description "Lunch" --amount 20
#   list expenses --> expense-tracker list
#   summary all expenses --> expense-tracker summary
#   summary all month expenses --> expense-tracker summary --month 8
#   delete expense --> expense-tracker delete --id 2

# json file as db file: is not the optimal choice
# but is for learning how to use json.

# argparse or prompt_toolkit for CLI
# custom functions for formatting list table
# (based on automate boring stuff with python)

# step 1: implement JSON DB
# step 2: implement add expense entries
#   step 2.1: assert values
#   step 2.2: implement datetime type and assert.
# step 3: implement delete expense
# step 4: implement summary
#   step 4.1: all expenses
#   step 4.2: all month expenses
# step 5: implement list expenses
# step 6: implement CLI
# step 7: implement list format

# expense table example
# ID | Date       | Description | Amount
# ---------------------------------------
# 1  | 2024-08-06 | Lunch       | $20
# 2  | 2024-08-06 | Dinner      | $10
# 3  | 2024-08-06 | Uber        | $7
# 4  | 2024-08-06 | Supermarket | $20
# 5  | 2024-08-06 | Restaurant  | $35
# 6  | 2024-08-06 | Dinner      | $12

# json db



def create_db(db_path):
    """Create JSON Database, only if not exists."""
    if db_path.exists():
        #print("File exists.")
        pass
    else:
        print("File does not exists.")
        with open(db_path, 'a'):
            print(f"json db created succesfully")


def save_db(db_path, expenses_list):
    """Save list of dictionaries to JSON file."""
    with open(db_path, 'w') as db_file:
        json.dump(expenses_list,db_file, indent=2)
        #print("saved data to json file.")

def open_db(db_path):
    """Open JSON File and returns its data."""
    with open(db_path, 'r') as db_file:
        expenses_list = json.load(db_file)
    return expenses_list

def assert_expense_data_types(id, date, description, amount):
    """Assert data types for expense entry."""
    assert(type(id) == int)
    assert(type(date) == str)
    assert(type(description) == str)
    assert(type(amount) == int)
           
def check_repeated_expense_id(expenses_list, new_id):
    """Check if expense ID is repeated in the expenses_list. 
        Returns True if repeated. Returns False if not repeated."""
    is_repeated = False
    for expense in expenses_list:
        current_id = expense["expense"]["id"]
        if current_id == new_id:
            is_repeated = True
            break #el id está repetido, cambia el estado y termina el loop
    return is_repeated

def get_last_expense_id(expenses_list):
    """Get the ID of the last expense entry in Expenses List."""
    return expenses_list[-1]["expense"]["id"]

def add_expense_to_db_auto_id(db_path, date, description, amount):
    """Add Expense entry to JSON database, without needing to specify ID."""
    expenses_list = open_db(db_path)
    id = get_last_expense_id(expenses_list) + 1
    assert_expense_data_types(id, date, description, amount)
    expense = {"expense": {"id":id,
                           "date":date,
                           "description":description,
                           "amount":amount}}
    #add new entry
    if not check_repeated_expense_id(expenses_list, id):
        expenses_list.append(expense) 
        save_db(db_path, expenses_list)
        print("added expense correctly.")
    else:
        print("cannot add expense because id is repeated.")

def add_expense_to_db(db_path, id, date, description, amount):
    """Add Expense entry to JSON database. Needs to specify ID."""
    assert_expense_data_types(id, date, description, amount)
    expense = {"expense": {"id":id,
                           "date":date,
                           "description":description,
                           "amount":amount}}
    expenses_list = open_db(db_path)
    
    #add new entry
    if not check_repeated_expense_id(expenses_list, id):
        expenses_list.append(expense) 
        save_db(db_path, expenses_list)
        print("added expense correctly.")
    else:
        print("cannot add expense because id is repeated.")


if __name__ == "__main__":

    database_filename = "expense_db.json"
    current_dir = Path.cwd()
    db_path = Path(current_dir) / database_filename
    create_db(db_path)
    add_expense_to_db(db_path, 10, "05-21-2026","comida", 4500)
    add_expense_to_db_auto_id(db_path,"05-21-2026","comida", 4500)

