# Archivo para definir funciones relacionadas a la línea de comando
import argparse

def init_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug","-d",action="store_true")
    #list
    parser.add_argument("list",nargs="?")

    subparsers = parser.add_subparsers(dest="action")

    #add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description",type=str)
    add_parser.add_argument("--amount",type=int)

    #delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("task_id",type=int)

    
  
    #summary
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--year",type=int)
    summary_parser.add_argument("--month",type=int)

    return parser

def parse_args_to_dict(parser):
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    parser = init_cli()
    args = parse_args_to_dict(parser)
    print(args)