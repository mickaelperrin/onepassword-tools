from onepassword_tools.lib.OnePasswordServerItem import OnePasswordServerItem
from onepassword_tools.lib.NewItemCommand import NewItemCommand, new_item_command_options, new_item_command_password
import click


@click.command()
@new_item_command_options
@new_item_command_password
@click.option('--hostname', help='Host where the account is created', prompt=True, required=True)
@click.option('--username', help='Account username', prompt=True, required=True)
def new_server_account(hostname, username, password, password_length, vault, return_field, account, title, notes, do_not_ask_credentials):
    """Create a new Server item in 1Password with the given credentials."""
    NewServerAccount(**locals()).run()


class NewServerAccount(NewItemCommand):

    hostname: str = None
    onePasswordItemClass = OnePasswordServerItem
    titleTemplate = 'USER {username} ON {hostname}'
    username: str = None


