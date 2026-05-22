# expense-tracker 
import json
import os
from pathlib import Path
import datetime as dt
import logging

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

# step 1: implement JSON DB ✅
# step 2: implement add expense entries
#   step 2.1: assert values ✅
#   step 2.2: implement datetime type and assert. ✅ Only asserts at entry, but not at
#                                                    at retrieval from JSON file.
# step 3: implement delete expense ✅
# step 4: implement summary
#   step 4.1: all expenses ✅
#   step 4.2: all month expenses
#   step 4.3: format value to CLP format
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
        logging.debug("[FUNCTION] (create_db) File exists.")
    else:
        logging.debug("[FUNCTION] (create_db) File does not exists.")
        with open(db_path, 'a'):
            logging.debug(f"[FUNCTION] (create_db) json db created succesfully")


def save_db(db_path, expenses_list):
    """Save list of dictionaries to JSON file."""
    with open(db_path, 'w') as db_file:
        json.dump(expenses_list,db_file, indent=2)
        logging.debug("[FUNCTION] (save_db) saved data to json file.")

def open_db(db_path):
    """Open JSON File and returns its data."""
    with open(db_path, 'r') as db_file:
        expenses_list = json.load(db_file)
    
    logging.debug(f"[FUNCTION] (open_db) expenses_list content:")
    logging.debug(expenses_list)
    return expenses_list

def assert_expense_data_types(id, date, description, amount):
    """Assert data types for expense entry."""
    assert(type(id) == int)
    assert(type(date) == dt.datetime)
    assert(type(description) == str)
    assert(type(amount) == int)
           
def check_repeated_expense_id(expenses_list, new_id):
    """Check if expense ID is repeated in the expenses_list. 
        Returns True if repeated. Returns False if not repeated."""
    is_repeated = False
    if len(expenses_list) > 0:
        for expense in expenses_list:
            current_id = expense["expense"]["id"]
            if current_id == new_id:
                is_repeated = True
                break #el id está repetido, cambia el estado y termina el loop
    return is_repeated

def get_last_expense_id(expenses_list):
    """Get the ID of the last expense entry in Expenses List."""
    logging.debug(f"[FUNCTION] (get_last_expense_id) expenses_list length: {len(expenses_list)}.")
    last_id = expenses_list[-1]["expense"]["id"] if len(expenses_list) > 0 else 0
    logging.debug(f"[FUNCTION] (get_last_expense_id) last expense ID: {last_id}")
    return last_id

def add_expense_to_db(db_path, id, date, description, amount):
    """Add Expense entry to JSON database. Needs to specify ID."""
    assert_expense_data_types(id, date, description, amount)
    expense = {"expense": {"id":id,
                           "date":date.strftime("%Y-%m-%d %H:%M:%S"),
                           "description":description,
                           "amount":amount}}
    expenses_list = open_db(db_path)
    #add new entry
    if not check_repeated_expense_id(expenses_list, id):
        expenses_list.append(expense) 
        save_db(db_path, expenses_list)
        logging.debug("[FUNCTION] (add_expense_to_db) added expense correctly.")
    else:
        logging.debug("[FUNCTION] (add_expense_to_db) cannot add expense because id is repeated.")

def add_expense_to_db_auto(db_path, description, amount):
    """Add Expense entry to JSON database, without needing to specify ID nor date."""
    expenses_list = open_db(db_path)
    id = get_last_expense_id(expenses_list) + 1
    logging.debug(f"[FUNCTION] (add_expense_to_db_auto) new expense ID: {id}.")
    date = dt.datetime.now()
    add_expense_to_db(db_path, id, date, description, amount)
  
def delete_expense(db_path, id):
    expenses_list = open_db(db_path)
    is_found = False
    id_list_index = 0
    for list_index, expense in enumerate(expenses_list):
        expense_id = expense["expense"]["id"]
        if expense_id == id:
            is_found = True
            id_list_index = list_index
            break
    if is_found:
        expenses_list.pop(id_list_index)
        save_db(db_path, expenses_list)
        logging.info(f"[FUNCTION] (delete_expense) Expense Index {id} deleted.")
    else:
        logging.info(f"[FUNCTION] (delete_expense) Index {id} NOT found. Cannot delete.")

def summary_expenses(db_path):
    expenses_list = open_db(db_path)
    summary = 0
    for expense in expenses_list:
        currentAmount = expense["expense"]["amount"]
        summary += currentAmount
    return summary

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    database_filename = "expense_db.json"
    current_dir = Path.cwd()
    db_path = Path(current_dir) / database_filename
    create_db(db_path)
    add_expense_to_db_auto(db_path, "comida",4512)
    delete_expense(db_path,3)
    summary = summary_expenses(db_path)
    print(f"Total Expenses: ${summary}")
