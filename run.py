# run.py
from pathlib import Path

from shell.controller.rw_handler import load_log
from shell.controller.database import Database
from shell.controller.parser import create_parser
from shell.view.cli import QShell

# Paths to the root of the project and the `data` subfolder.
ROOT_PATH = Path.cwd().resolve()
DATA_PATH = ROOT_PATH / 'data'

def main():
    arg_parser, query_parser = create_parser()
    args = arg_parser.parse_args()

    # Load log file into database application
    log_file = DATA_PATH / args.log_file
    database = Database(load_log(log_file))

    # Run shell interface
    QShell(database, query_parser, DATA_PATH).cmdloop()


if __name__ == '__main__':
    main()
