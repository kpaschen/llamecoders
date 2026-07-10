"""Tests for CLI module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from costscraper.cli import main

def makeConfigContent(inputCost=7e-7, outputCost=25e-7):
    return (
        "model_list:\n"
        "  - model_name: infomaniak-qwen3.5-122b\n"
        "    litellm_params:\n"
        "       custom_llm_provider: openai\n"
        "       model: Qwen/Qwen3.5-122B-A10B-FP8\n"
        "       api_base: https://api.infomaniak.com/2/ai/109660/openai/v1\n"
        "       api_key: os.environ/INFOMANIAK_API_KEY\n"
        "    model_info:\n"
        f"       input_cost_per_token: {inputCost}\n"
        f"       output_cost_per_token: {outputCost}\n"
        "\n"
        "  - model_name: gpt-4o\n"
        "    litellm_params:\n"
        "       model: openai/gpt-4o\n"
        "       api_key: os.environ/OPENAI_API_KEY\n"
        "       rpm: 2\n"
    )


def testCliDryRun():
    runner = CliRunner()
    configText = makeConfigContent(inputCost=7e-7, outputCost=25e-7)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(configText)
        configPath = f.name

    mockPrices = {"Qwen/Qwen3.5-122B-A10B-FP8": {"input": 4e-7, "output": 3e-6}}
    with patch("costscraper.cli.InfomaniakFetcher.fetchPrices", return_value=mockPrices):
        result = runner.invoke(main, ["--config", configPath, "--dry-run"])

    assert result.exit_code == 0
    assert "Dry run complete" in result.output
    assert "Qwen/Qwen3.5-122B-A10B-FP8" in result.output

    # Verify file untouched
    with open(configPath, "r") as f:
        content = f.read()
    assert "input_cost_per_token: 7e-07" in content or "input_cost_per_token: 0.0000007" in content

    Path(configPath).unlink()


def testCliUpdate():
    runner = CliRunner()
    configText = makeConfigContent(inputCost=7e-7, outputCost=25e-7)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(configText)
        configPath = f.name

    mockPrices = {"Qwen/Qwen3.5-122B-A10B-FP8": {"input": 4e-7, "output": 3e-6}}
    with patch("costscraper.cli.InfomaniakFetcher.fetchPrices", return_value=mockPrices):
        result = runner.invoke(main, ["--config", configPath])

    assert result.exit_code == 0
    assert "Config updated successfully" in result.output

    with open(configPath, "r") as f:
        content = f.read()
    assert "0.0000007" not in content

    Path(configPath).unlink()


def testCliFetcherWarning():
    runner = CliRunner()
    configText = makeConfigContent(inputCost=7e-7, outputCost=25e-7)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(configText)
        configPath = f.name

    with patch(
        "costscraper.cli.InfomaniakFetcher.fetchPrices",
        side_effect=Exception("network down"),
    ):
        result = runner.invoke(main, ["--config", configPath])

    assert result.exit_code == 0
    assert "Warning" in result.output
    assert "network down" in result.output
    assert "No pricing updates detected" in result.output

    # File must remain untouched
    with open(configPath, "r") as f:
        content = f.read()
    assert "input_cost_per_token: 7e-07" in content or "input_cost_per_token: 0.0000007" in content

    Path(configPath).unlink()


def testCliMissingConfig():
    runner = CliRunner()
    result = runner.invoke(main, ["--config", "/does/not/exist.yaml"])
    assert result.exit_code != 0
    assert "does not exist" in result.output or "Invalid value" in result.output


def testCliNoPricedModels():
    runner = CliRunner()
    config = (
        "model_list:\n"
        "  - model_name: gpt-4o\n"
        "    litellm_params:\n"
        "       model: openai/gpt-4o\n"
        "       api_key: os.environ/OPENAI_API_KEY\n"
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(config)
        configPath = f.name

    result = runner.invoke(main, ["--config", configPath])
    assert result.exit_code == 0
    assert "No models with existing pricing found" in result.output

    Path(configPath).unlink()
