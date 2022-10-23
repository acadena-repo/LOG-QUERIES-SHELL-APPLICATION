# cli.py
import sys
import cmd
import shlex

from ..controller.filters import create_filters, limit
from ..controller.rw_handler import write_to_csv

def query(database, root, args):
    """Perform the `query` subcommand.

    Create a collection of filters with `create_filters` and supply them to the
    database's `query` method to produce a stream of matching results.

    If an output file wasn't given, print these results to stdout. 
    If an output file was given, write the results to output file in CSV format.

    :param database: The `Database` containing the logged events records.
    :param args: All arguments from the command line, as parsed by the top-level parser.
    """
    if args.head is not None and args.head > 0:
        results = database.get_head(args.head)
        for x, result in enumerate(results):
            print(f'{x + 1}: {result}')

    elif args.tail is not None and args.tail > 0:
        results = database.get_tail(args.tail)
        for x, result in enumerate(results):
            print(f'{x + 1}: {result}')
    else:
        # Construct a collection of filters from arguments supplied at the command line.
        filters = create_filters(start_date=args.start_date, end_date=args.end_date,
                                severity=args.severity, code=args.code)
        # Query the database with the collection of filters.
        results = database.query(filters)

        if not args.outfile:
            # Write the results to stdout.
            for x, result in enumerate(limit(results, args.limit)):
                print(f'{x + 1}: {result}')
        else:
            # Write the results to a file.
            opath = root / args.outfile

            if opath.suffix == '.csv':
                write_to_csv(limit(results, args.limit), opath)
            else:
                print("Please use an output file that ends with `.csv`", file=sys.stderr)


class QShell(cmd.Cmd):
    '''Perform an `interactive` command-base interface.

    It wraps the `query` parser to parse flags for those commands
    as if they were supplied at the command line.

    The primary purpose of this shell is to allow users to repeatedly perform
    query commands, while only loading the data (which can be quite slow) once.
    '''
    intro = (
        '''
           ____   _____ __         ____
          / __ \ / ___// /_  ___  / / /
         / / / / \__ \/ __ \/ _ \/ / / 
        / /_/ / ___/ / / / /  __/ / /  
        \___\_\/____/_/ /_/\___/_/_/                    
         __   ____  ______                
        / /  / __ \/ ____/                
       / /  / / / / / __                  
      / /__/ /_/ / /_/ /                  
     /_____|____/\____/______  __________ 
        / ____/  _/ | / / __ \/ ____/ __ \\
       / /_   / //  |/ / / / / __/ / /_/ /
      / __/ _/ // /|  / /_/ / /___/ _, _/ 
     /_/   /___/_/ |_/_____/_____/_/ |_|   

    Type `help` or `?` to list commands and `exit` to exit.\n                                
        '''
    )
    prompt = '>>> '

    def __init__(self, database, parser, root, **kwargs):
        """Create a new `QShell`.

        Creating this object doesn't start the session - for that, use `.cmdloop()`.

        :param database: The `NEODatabase` containing data on NEOs and their close approaches.
        :param inspect_parser: The subparser for the `inspect` subcommand.
        :param query_parser: The subparser for the `query` subcommand.
        :param aggressive: Whether to kill the session whenever a project file is changed.
        :param kwargs: A dictionary of excess keyword arguments passed to the superclass.
        """
        super().__init__(**kwargs)
        self.db = database
        self.query = parser
        self._root = root

    @classmethod
    def parse_arg_with(cls, arg, parser):
        '''Parse the additional text passed to a command, using a given parser.

        If any error is encountered (in lexical parsing or argument parsing),
        print the error to stderr and return None.

        :param arg: The additional text supplied after the command.
        :param parser: An `argparse.ArgumentParser` to parse the arguments.
        :return: A `Namespace` of the arguments (produced by `parse_args`) or None.
        '''
        # Lexically parse the additional text with POSIX shell-like syntax.
        try:
            args = shlex.split(arg)
        except ValueError as err:
            print(err, file=sys.stderr)
            return None

        # Use the ArgumentParser to parse the shell arguments.
        try:
            return parser.parse_args(args)
        except SystemExit as err:
            return None

    def do_query(self, arg):
        '''Perform the `query` subcommand'''

        args = self.parse_arg_with(arg, self.query)
        if not args:
            return

        # Run the `query` subcommand.
        query(self.db, self._root, args)
    
    def help_query(self):
        message = '''
        query [-h] [--head HEAD] [--tail TAIL] [--start-date START_DATE] [--end-date END_DATE] [--severity {ERROR,WARNING,INFO}] [--code CODE] [--limit LIMIT] [--outfile OUTFILE]

        Query operations for log events that match a collection of filters.

        options:
        -h, --help            show this help message and exit
        --head HEAD           Return the first records according to the number specified.
        --tail TAIL           Return the last records according to the number specified.
        --limit LIMIT         The maximum number of matches to return.
        --outfile OUTFILE     File in which to save query results. If omitted, results are printed to standard output.

        Filters:
        Filter log events by their attributes.

        --start-date START_DATE
                                Return logged events on or after the given date, in YYYY-MM-DD HH:MM:SS format (e.g. 2020-12-31 23:59:59).
        --end-date END_DATE   Return logged events on or before the given date, in YYYY-MM-DD HH:MM:SS format (e.g. 2020-12-31 23:59:59).
        --severity {ERROR,WARNING,INFO}
                                Return logged events that contains the severity level specified
        --code CODE           Return logged events that contains the validation error code specified
        '''
        print(message)

    def do_exit(self, _exit):
        '''Exit the interactive session.'''
        return True