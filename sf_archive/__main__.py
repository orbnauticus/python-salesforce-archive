#!/usr/bin/env python3

"""
Command line client
"""

import argparse

from . import SalesforceArchive


parser = argparse.ArgumentParser()

subparser = parser.add_subparsers()


def do_extract(args):
    """
    Extract a data export
    """
    SalesforceArchive.extract(args.archive, args.extract_to)

parser_extract = subparser.add_parser('extract')
parser_extract.add_argument('archive')
parser_extract.add_argument('extract_to', nargs='?', default='.')
parser_extract.set_defaults(command=do_extract)


args = parser.parse_args()

args.command(args)

# print(archive.tables.keys())

# for row in archive.tables['Attachment']:
#     print(row)
