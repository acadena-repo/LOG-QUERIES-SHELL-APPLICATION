# parser.py
import argparse
from pathlib import Path

from ..support.utilities import date_fromisoformat

def create_parser():
    """Create an ArgumentParser for this script.

    :return: A tuple of the top-level, inspect, and query parsers.
    """
    parser = argparse.ArgumentParser(
        description="Inspection and query of log events during the validation of an ETL process."
    )
    parser.add_argument('log_file', type=Path,
                        help="Path to log file to be inspected.")

    subparser = parser.add_subparsers(dest='commad')

    # Adding `query` subcommand parser.
    query = subparser.add_parser('query', description="Query operations for log events that match a collection of filters.")

    query.add_argument('--head', type=int,
                       help="Return the first records according to the number specified.")
    query.add_argument('--tail', type=int,
                       help="Return the last records according to the number specified.")  

    filters = query.add_argument_group('Filters', description="Filter log events by their attributes.")

    filters.add_argument('--start-date', type=date_fromisoformat,
                         help="Return logged events on or after the given date, "
                              "in YYYY-MM-DD HH:MM:SS format (e.g. '2020-12-31 23:59:59').")
    filters.add_argument('--end-date', type=date_fromisoformat,
                         help="Return logged events on or before the given date, "
                              "in YYYY-MM-DD HH:MM:SS format (e.g. '2020-12-31 23:59:59').")
    filters.add_argument('--severity', type=str, choices=['ERROR','WARNING','INFO'],
                         help="Return logged events that contains the severity level specified")
    filters.add_argument('--code', type=str,
                         help="Return logged events that contains the validation error code specified")
                  
    query.add_argument('--limit', type=int,
                       help="The maximum number of matches to return.")
    query.add_argument('--outfile', type=Path,
                       help="File in which to save query results. "
                            "If omitted, results are printed to standard output.")

    return parser, query

