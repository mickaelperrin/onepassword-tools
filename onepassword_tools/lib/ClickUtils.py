import click


class ClickUtils:

    @staticmethod
    def error(message):
        click.echo(click.style(message, fg='red', bold=True))

    @staticmethod
    def info(message):
        click.echo(message)

    @staticmethod
    def success(message):
        click.echo(click.style(message, fg='green'))