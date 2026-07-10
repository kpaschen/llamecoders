"""costscraper CLI entry point."""

import sys

import click

from .config import loadConfig, saveConfig, findModelsWithPricing, updateModelPricing
from .fetchers.infomaniak import InfomaniakFetcher
from .mapping import ModelMapper


def formatPrice(value):
    formatted = format(float(value), ".12f")
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    if formatted == "-0":
        formatted = "0"
    return formatted


@click.command()
@click.option(
    "--config",
    "configPath",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    help="Path to litellm-config.yaml to read and update.",
)
@click.option(
    "--dry-run",
    "dryRun",
    is_flag=True,
    default=False,
    help="Preview changes without writing to the config file.",
)
def main(configPath, dryRun):
    """Fetch current LLM pricing and update litellm-config.yaml."""
    try:
        configData = loadConfig(configPath)
    except Exception as exc:
        click.echo(f"Error loading config: {exc}", err=True)
        sys.exit(1)

    pricedModels = findModelsWithPricing(configData)
    if not pricedModels:
        click.echo("No models with existing pricing found in config.")
        sys.exit(0)

    mapper = ModelMapper()
    fetchers = [InfomaniakFetcher(mapper=mapper)]

    allPrices = {}
    for fetcher in fetchers:
        try:
            prices = fetcher.fetchPrices()
        except Exception as exc:
            click.echo(
                f"Warning: failed to fetch prices from {fetcher.__class__.__name__}: {exc}",
                err=True,
            )
            continue
        allPrices.update(prices)

    updatedModels = updateModelPricing(configData, allPrices, dryRun=dryRun)

    if not updatedModels:
        click.echo("No pricing updates detected.")
        sys.exit(0)

    for info in updatedModels:
        click.echo(
            f"{info['modelName']} ({info['modelId']}): "
            f"input {formatPrice(info['oldInput'])} -> {formatPrice(info['newInput'])}, "
            f"output {formatPrice(info['oldOutput'])} -> {formatPrice(info['newOutput'])}"
        )

    if dryRun:
        click.echo("\nDry run complete; no changes written.")
    else:
        try:
            saveConfig(configPath, configData)
            click.echo("\nConfig updated successfully.")
        except Exception as exc:
            click.echo(f"Error saving config: {exc}", err=True)
            sys.exit(1)


if __name__ == "__main__":
    main()
