import click
import json

import src.app


@click.command()
@click.option(
    "-c",
    "--config",
    required=True,
    type=click.Path(
        exists=True,
        readable=True,
        resolve_path=True
    ),
    help="Config file path.")
def cli(
        config: str,
) -> None:
    config_json: dict

    with open(config, "r") as config_file:
        config_json = json.load(config_file)

    src.app.run(
        config=config_json
    )


if __name__ == "__main__":
    cli()
