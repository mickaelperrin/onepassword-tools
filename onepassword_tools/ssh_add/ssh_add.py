import click
from onepassword_local_search.OnePassword import OnePassword
from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils


@click.command()
def ssh_add():
    SSHAdd().run()


class SSHAdd:

    sessionKey: str
    onePassword: OnePassword

    def __init__(self):
        self.onePasswordUtils = OnePasswordUtils()

    def run(self):
        if not self.onePasswordUtils.is_authenticated():
            self.onePasswordUtils.authenticate()
        click.echo('ssh-add')
