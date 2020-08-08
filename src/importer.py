"""
importer module

Imports a KDBX into another KDBX
"""

import argparse
import os

from pykeepass import pykeepass as kp

DESCRIPTION = ''' Imports Keepass Data into a KDBX database '''


def parse_command_line(args: list):
    """
    Parses the command line arguments
    :param args: The arguments
    :return:
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=DESCRIPTION,
    )
    parser.add_argument(
        'source-database',
        dest='source_database',
        nargs=1,
        metavar='SOURCE',
        help='The source database file',
        type=str
    )
    parser.add_argument(
        'target-database',
        dest='target_database',
        nargs=1,
        metavar='TARGET',
        help='The target database file',
        type=str
    )
    parser.add_argument(
        '-k', '--source-keyfile',
        dest='source_keyfile',
        help='The keyfile required to decrypt the source database',
        type=str,
        required=False
    )
    parser.add_argument(
        '-l', '--target-keyfile',
        dest='target_keyfile',
        help='The keyfile required to decrypt the target database',
        type=str,
        required=False
    )
    return parser.parse_args(args)


def create_database(filename: str,
                    password: str,
                    keyfile: str or None = None):
    """
    Creates a new KDBX database

    :param filename: The database filename
    :param password: The database password
    :param keyfile:  An optional keyfile
    :return: A PyKeePass object
    """
    return kp.create_database(
        filename,
        password,
        keyfile
    )


def open_database(filename: str,
                  password: str,
                  keyfile: str or None = None):
    """
    Opens a KDBX database

    :param filename: The database filename
    :param password: The database password
    :param keyfile:  An optional keyfile
    :return: A PyKeePass object
    """
    return kp.PyKeePass(
        filename,
        password,
        keyfile
    )


def close_database(database: kp.PyKeePass,
                   save=True):
    """
    Closes a KDBX database

    :param database: The database to be closed
    :param save:     Force a save operation prior closing
    """
    if save:
        database.save()
    del database


def import_entries(target_database: kp.PyKeePass,
                   source_database: kp.PyKeePass):
    """
    Imports entries from the source database into a target database

    :param target_database: The target database where entries get imported
    :param source_database: The source database which provides
                            entries to be imported
    """
    print(source_database.root_group)
    print(target_database.root_group)


def read_password(prompt='Password: ') -> str:
    """
    Reads a password from a CLI prompt

    :param prompt: The prompt string presented to the user
    :return:       The data entered by the user
    """
    return input(prompt)


def run(args: list) -> int:
    """
    Runs the import

    :param args: The cli arguments
    :return:     An exit code, EX_OK means success
    """
    cli = parse_command_line(args)
    print(cli)

    source_password = read_password('Password for Source database: ')
    target_password = read_password('Password for Target database: ')

    source_database = open_database(
        cli.source_database,
        source_password,
        cli.source_targetfile
    )
    target_database = open_database(
        cli.target_database,
        target_password,
        cli.target_keyfile
    )

    import_entries(target_database, source_database)

    close_database(target_database, True)
    close_database(source_database, False)

    return os.EX_OK
