from argparse import ArgumentParser
import sys

from pykeepass import pykeepass as kp

DESCRIPTION = ''' Imports Keepass Data into a KDBX database '''


def parse_command_line(args: list):
    """
    Parses the command line arguments
    :param args: The arguments
    :return:
    """
    parser: ArgumentParser = ArgumentParser(
        description=DESCRIPTION,
    )
    parser.add_argument(
        'source-database',
        nargs=1,
        metavar='SOURCE',
        help='The source database file',
        type=str
    )
    parser.add_argument(
        'target-database',
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
    parser.add_argument(
        '-c', '--target-create',
        dest='target_create',
        help='Create a new target database',
        action='store_true',
        required=False
    )
    return parser.parse_args(args)


def create_database(database: str, password: str, keyfile: str or None = None):
    return kp.create_database(database, password, keyfile)


def open_database(database: str, password: str, keyfile: str or None = None):
    return kp.PyKeePass(database, password, keyfile)


def close_database(database: kp.PyKeePass, save=True):
    if save:
        database.save()
    del database


def import_entries(database: kp.PyKeePass):
    database.root_group
    pass


def read_password(prompt='Password: ') -> str:
    return input(prompt)


def run(args: list) -> None:
    cli = parse_command_line(args)
    print(cli)

    source_password = read_password('Password for Source database: ')
    target_password = read_password('Password for Target database: ')

    print(source_password)
    print(target_password)
