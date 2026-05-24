# Archivo para definir funciones relacionadas a la línea de comando
import argparse

def init_cli():
    parser = argparse.ArgumentParser("Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # allowed operations
#   add expenses --> expense-tracker add --description "Lunch" --amount 20
#   list expenses --> expense-tracker list
#   summary all expenses --> expense-tracker summary
#   summary all month expenses --> expense-tracker summary --month 8
#   delete expense --> expense-tracker delete --id 2

    add_cmd = subparsers.add_parser("add",help="add expense")
    add_cmd.add_argument("--description",help="Description of expense",required=True)
    add_cmd.add_argument("--amount",help="expense amount",type=int,required=True)

    list_cmd = subparsers.add_parser("list",help="list all expenses")

    summary_cmd = subparsers.add_parser("summary",help="summary expenses")
    summary_cmd.add_argument("--month",type=int,help="month to retrieve expenses")
    summary_cmd.add_argument("--year",help="year to retrieve expenses",type=int)
    
    update_cmd = subparsers.add_parser("update",help="update expense")
    update_cmd.add_argument("--id",help="expense of id to update",type=int)
    update_cmd.add_argument("--description",help="updated description of expense")
    update_cmd.add_argument("--amount",help="updated expense amount",type=int)


    delete_cmd = subparsers.add_parser("delete",help="delete expense by ID")
    delete_cmd.add_argument("--id",help="expense's ID to delete",type=int,required=True)

    args = parser.parse_args()

   
    #handle summary error where only year or month is provided. It 
    #should be both or none.
    if args.command == "summary":
        month_provided = args.month is not None
        year_provided = args.year is not None

        if month_provided != year_provided:
            summary_cmd.error("--month and --year must be used together.")   

    return args


if __name__ == "__main__":
    args = init_cli()
    print(args)