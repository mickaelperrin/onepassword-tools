#!/usr/bin/env python3
import click
import click_log
from onepassword_tools.ssh_add import ssh_add
from onepassword_tools.new_server_account import new_server_account
from onepassword_tools.new_ssh_key import new_ssh_key
from onepassword_tools.new_website_account import new_website_account
from onepassword_tools.new_database_account import new_database_account
from onepassword_tools.lib.Log import logger
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger)
def start():
    pass


start.add_command(ssh_add.ssh_add)
start.add_command(new_server_account.new_server_account)
start.add_command(new_ssh_key.new_ssh_key)
start.add_command(new_website_account.new_website_account)
start.add_command(new_database_account.new_database_account)

if __name__ == '__main__':
    start()
