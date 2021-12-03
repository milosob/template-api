import click
import json

import src.app


@click.command()
@click.option(
    "-c",
    "--config-path",
    required=True,
    type=click.Path(
        exists=True,
        readable=True,
        resolve_path=True
    ),
    help="Config file path.")
def cli(
        config_path: str,
) -> None:
    config: dict

    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    src.app.run(
        config=config
    )


if __name__ == "__main__":
    cli()
