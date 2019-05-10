from onepassword_tools.lib.OnePasswordDatabaseItem import OnePasswordDatabaseItem
from onepassword_tools.lib.NewItemCommand import NewItemCommand, new_item_command_options, new_item_command_password
import click


@click.command()
@new_item_command_options
@new_item_command_password
@click.option('--database', help='Database name', prompt=False, required=True)
@click.option('--hostname', help='Host where the account is created', prompt=True, required=True)
@click.option('--port', help='Database port', prompt=False, required=False, default='')
@click.option('--username', help='Account username', prompt=True, required=True)
def new_database_account(hostname, database, port, username, account, notes, password, password_length, return_field, title, vault, do_not_ask_credentials):
    """Create a new Database item in 1Password with the given credentials."""
    NewDatabaseAccount(**locals()).run()


class NewDatabaseAccount(NewItemCommand):

    database: str = None
    hostname: str = None
    port: str = None
    titleTemplate = 'USER {username} DB {database} ON {hostname}'
    username: str = None
    onePasswordItemClass = OnePasswordDatabaseItem
