import click


class ClickUtils:

    @staticmethod
    def error(message):
        click.echo(click.style(message, fg='red', bold=True))
