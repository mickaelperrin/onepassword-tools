from onepassword_tools.lib.OnePasswordLoginItem import OnePasswordLoginItem
from onepassword_tools.lib.NewItemCommand import NewItemCommand, new_item_command_options, new_item_command_password
import click


@click.command()
@new_item_command_options
@new_item_command_password
@click.option('--url', help='URL of the website where the account is created', prompt=True, required=True)
@click.option('--username', help='Account username', prompt=True, required=True)
def new_website_account(url, title, username, password, password_length, return_field, vault, account, notes, do_not_ask_credentials):
    """Create a new Login item in 1Password with the given credentials."""
    NewWebsiteAccount(**locals()).run()


class NewWebsiteAccount(NewItemCommand):

    hostname: str = None
    onePasswordItemClass = OnePasswordLoginItem
    titleTemplate = 'ACCOUNT {username} ON {url}'
    url: str = None
    username: str = None

