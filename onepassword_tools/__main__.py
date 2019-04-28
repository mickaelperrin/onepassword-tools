#!/usr/bin/env python3
import click
from onepassword_tools.ssh_add import ssh_add
from onepassword_tools.new_server_password import new_server_password


@click.group()
def start():
    pass


start.add_command(ssh_add.ssh_add)
start.add_command(new_server_password.new_server_password)

if __name__ == '__main__':
    start()
