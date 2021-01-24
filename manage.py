import click
from views import create_app

cli = click.Group()


@cli.command()
@click.option('--debug', '-d', is_flag=True, default=False)
def runserver(debug):
    app = create_app()
    app.run(debug=debug, port=8080)


if __name__ == '__main__':
    cli.main()