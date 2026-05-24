# expense-tracker 
import json
import os
from pathlib import Path
import datetime as dt
import logging
import cli
import sys
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import HTML

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
#   step 4.2: all month expenses ✅
#   step 4.3: format value to CLP format ✅
# step 5: implement list expenses ✅
# step 6: implement CLI ✅
# step 7: implement list format ✅ 

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
        with open(db_path, 'a') as db_file:
            json.dump([],db_file, indent=2)
            logging.debug(f"[FUNCTION] (create_db) json db created succesfully")


def save_db(db_path, expenses_list):
    """Save list of dictionaries to JSON file."""
    with open(db_path, 'w') as db_file:
        json.dump(expenses_list,db_file, indent=2)
        logging.debug("[FUNCTION] (save_db) saved data to json file.")

def open_db(db_path):
    """Open JSON File and returns its data."""
    try:
        with open(db_path, 'r') as db_file:
            expenses_list = json.load(db_file)
        
        logging.debug(f"[FUNCTION] (open_db) expenses_list content:")
        logging.debug(expenses_list)
        return expenses_list
    except json.decoder.JSONDecodeError:
        print("Error reading JSON File. Maybe it's corrupted",file=sys.stderr)
        sys.exit(1)

def assert_expense_data_types(id, date, description, amount):
    """Assert data types for expense entry."""
    assert(type(id) == int and id >= 0)
    assert(type(date) == dt.datetime)
    assert(type(description) == str)
    assert(type(amount) == int and amount >= 0)

def check_if_db_is_empty(db_path):
    expenses_list = open_db(db_path)
    if len(expenses_list) == 0:
        print("Expense database is empty. Cannot make this operation",file=sys.stderr)
        sys.exit(0) 

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
        print(f"Added expense with ID: {id} correctly.")
    else:
        logging.debug("[FUNCTION] (add_expense_to_db) cannot add expense because id is repeated.")
        print("Cannot add expense because ID is repeated.")

def add_expense_to_db_auto(db_path, description, amount,date=dt.datetime.now()):
    """Add Expense entry to JSON database, without needing to specify ID nor date."""
    expenses_list = open_db(db_path)
    id = get_last_expense_id(expenses_list) + 1
    logging.debug(f"[FUNCTION] (add_expense_to_db_auto) new expense ID: {id}.")
    #date = dt.datetime.now()
    add_expense_to_db(db_path, id, date, description, amount)

def update_expense(db_path, id, new_date, new_description,new_amount,):
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
        expenses_list[id_list_index]["expense"]["date"] = new_date if new_date is not None else expenses_list[id_list_index]["expense"]["date"]
        expenses_list[id_list_index]["expense"]["description"] = new_description if new_description is not None else expenses_list[id_list_index]["expense"]["description"]
        expenses_list[id_list_index]["expense"]["amount"] = new_amount if new_amount is not None else expenses_list[id_list_index]["expense"]["amount"]
        save_db(db_path, expenses_list)
        logging.info(f"[FUNCTION] (delete_expense) Expense Index {id} updated.")
        print(f"Expense Index {id} updated.")
    else:
        logging.info(f"[FUNCTION] (delete_expense) Index {id} NOT found. Cannot update.")
        print(f"Index {id} NOT found. Cannot update.")

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
        logging.info(f"[FUNCTION] (update_expense) Expense Index {id} deleted.")
        print(f"Expense Index {id} deleted.")
    else:
        logging.info(f"[FUNCTION] (update_expense) Index {id} NOT found. Cannot delete.")
        print(f"Index {id} NOT found. Cannot delete.")

def amount_to_clp_str(amount):
    return f"${amount:,}".replace(",",".") + " CLP"

def summary_expenses(db_path):
    expenses_list = open_db(db_path)
    summary = 0
    if len(expenses_list) > 0:
        for expense in expenses_list:
            currentAmount = expense["expense"]["amount"]
            summary += currentAmount
    print("Total expenses: "+ f"{amount_to_clp_str(summary)}")

def summary_expenses_monthly(db_path, year,month):
    expenses_list = open_db(db_path)
    summary = 0
    if len(expenses_list) > 0:
        for expense in expenses_list:
            expense_date = dt.datetime.strptime(expense["expense"]["date"], "%Y-%m-%d %H:%M:%S")
            year_month_date = (expense_date.year,expense_date.month)

            if year_month_date == (year, month):
                currentAmount = expense["expense"]["amount"]
                summary += currentAmount
    print(f"Total expenses for {year}-{month:02d}: "+ f"{amount_to_clp_str(summary)}")

def find_largest_field(expenses_list):
    id_sublist = []
    date_sublist = []
    description_sublist = []
    amount_sublist = []
    for expense in expenses_list:
        id_sublist += [str(expense["expense"]["id"])]
        date_sublist += [expense["expense"]["date"]]
        description_sublist += [expense["expense"]["description"]]
        amount_sublist += [amount_to_clp_str(expense["expense"]["amount"])]
    
    field_largest_length = {"id":len(max(id_sublist,key=len)),
                            "date": len(max(date_sublist,key=len)),
                            "description":len(max(description_sublist,key=len)),
                            "amount":len(max(amount_sublist,key=len))}
    
    return field_largest_length

def list_expenses(db_path):
    expenses_list = open_db(db_path)
    if len(expenses_list) > 0:
        field_largest = find_largest_field(expenses_list)
        id_pad = field_largest["id"]
        date_pad = field_largest["date"]
        description_pad = max(field_largest["description"], len("Description"))
        amount_pad = field_largest["amount"]
        title = "Expenses"
        table_header = "ID".ljust(id_pad) + " | " + "Date".ljust(date_pad) + " | " + "Description".ljust(description_pad) +  " | " + "Amount".ljust(amount_pad) + " |\n"
        expenses_list_str = "\n"+ title + "\n" + table_header + "-"*len(table_header) + "\n"
        for expense in expenses_list:
            amount = expense["expense"]["amount"]
            id = expense["expense"]["id"]
            date = expense["expense"]["date"]
            description = expense["expense"]["description"]
            #expense_str = f"ID: {id:02d} - Date: {date} - Description: {description} - Amount: {amount_to_clp_str(amount)}\n"
            expense_str = f"{id:02d}".ljust(id_pad) + ' | ' + date.ljust(date_pad) + ' | ' + description.ljust(description_pad) + ' | ' + amount_to_clp_str(amount).ljust(amount_pad) + " |\n"
            expenses_list_str += expense_str
    else:
        title = "Expenses"
        table_header = "ID" + " | " + "Date" + " | " + "Description" +  " | " + "Amount" + " |\n"
        expenses_list_str = "\n"+ title + "\n" + table_header + "-"*len(table_header) + "\n"
    return expenses_list_str

def init_db(database_filename):
    #define db_name, create json file if don't exists
    current_dir = Path.cwd()
    db_path = Path(current_dir) / database_filename
    create_db(db_path)
    return db_path

if __name__ == "__main__":
    print(HTML('<ansired>This is red</ansired>'))
    #config basic logger for activate/desactivate print debugging
    logging.basicConfig(level=logging.INFO)

    database_filename = "expense_db.json"
    db_path = init_db(database_filename)

    args = cli.init_cli()
    logging.debug(args)

    if args.command == "update" or args.command == "delete":
        check_if_db_is_empty(db_path)
    
    if args.command == "add":
        description = args.description
        amount = args.amount
        add_expense_to_db_auto(db_path,description, amount)
    elif args.command == "list":
        list_str = list_expenses(db_path)
        print(list_str)
    elif args.command == "summary":
        summary = 0
        if args.month is not None and args.year is not None:
            month = args.month
            year = args.year
            summary_expenses_monthly(db_path, year, month)
        else:
            summary_expenses(db_path)
    elif args.command == "update":
        id = args.id
        new_date = None
        new_description = args.description
        new_amount = args.amount
        update_expense(db_path,id,new_date,new_description,new_amount)
    elif args.command == "delete":
        expense_id = args.id
        delete_expense(db_path, expense_id)
    

    