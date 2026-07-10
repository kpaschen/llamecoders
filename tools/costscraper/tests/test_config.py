"""Tests for config module."""

import tempfile
from pathlib import Path

from ruamel.yaml import YAML

from costscraper.config import (
    createYamlRoundTrip,
    loadConfig,
    saveConfig,
    findModelsWithPricing,
    updateModelPricing,
)


def testCreateYamlRoundTrip():
    yaml = createYamlRoundTrip()
    assert yaml.preserve_quotes is True


def testLoadAndSaveConfigRoundTrip():
    sample = (
        "model_list:\n"
        "  - model_name: test-model\n"
        "    litellm_params:\n"
        "       model: provider/test\n"
        "    model_info:\n"
        "       input_cost_per_token: 0.0000001\n"
        "       output_cost_per_token: 0.0000002\n"
        "# trailing comment\n"
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(sample)
        path = f.name

    data = loadConfig(path)
    saveConfig(path, data)

    with open(path, "r") as f:
        restored = f.read()

    assert "trailing comment" in restored
    Path(path).unlink()


def testFindModelsWithPricing():
    yaml = YAML()
    raw = (
        "model_list:\n"
        "  - model_name: open-model\n"
        "    litellm_params:\n"
        "       model: openai/gpt-4\n"
        "  - model_name: priced-model\n"
        "    litellm_params:\n"
        "       model: provider/test\n"
        "    model_info:\n"
        "       input_cost_per_token: 1.0e-7\n"
        "       output_cost_per_token: 2.0e-7\n"
    )
    data = yaml.load(raw)
    models = findModelsWithPricing(data)

    assert len(models) == 1
    assert models[0]["modelName"] == "priced-model"
    assert models[0]["modelId"] == "provider/test"
    assert models[0]["inputCost"] == 1.0e-7
    assert models[0]["outputCost"] == 2.0e-7


def testUpdateModelPricing():
    yaml = YAML()
    raw = (
        "model_list:\n"
        "  - model_name: priced-model\n"
        "    litellm_params:\n"
        "       model: provider/test\n"
        "    model_info:\n"
        "       input_cost_per_token: 1.0e-7\n"
        "       output_cost_per_token: 2.0e-7\n"
    )
    data = yaml.load(raw)
    newPrices = {"provider/test": {"input": 3.0e-7, "output": 4.0e-7}}

    updated = updateModelPricing(data, newPrices)

    assert len(updated) == 1
    assert updated[0]["newInput"] == 3.0e-7
    assert updated[0]["newOutput"] == 4.0e-7
    assert data["model_list"][0]["model_info"]["input_cost_per_token"] == 3.0e-7


def testUpdateModelPricingDryRun():
    yaml = YAML()
    raw = (
        "model_list:\n"
        "  - model_name: priced-model\n"
        "    litellm_params:\n"
        "       model: provider/test\n"
        "    model_info:\n"
        "       input_cost_per_token: 1.0e-7\n"
        "       output_cost_per_token: 2.0e-7\n"
    )
    data = yaml.load(raw)
    newPrices = {"provider/test": {"input": 3.0e-7, "output": 4.0e-7}}

    updated = updateModelPricing(data, newPrices, dryRun=True)

    assert len(updated) == 1
    # Original data must remain untouched
    assert data["model_list"][0]["model_info"]["input_cost_per_token"] == 1.0e-7


def testUpdateModelPricingMissingModel():
    yaml = YAML()
    raw = (
        "model_list:\n"
        "  - model_name: priced-model\n"
        "    litellm_params:\n"
        "       model: provider/test\n"
        "    model_info:\n"
        "       input_cost_per_token: 1.0e-7\n"
        "       output_cost_per_token: 2.0e-7\n"
    )
    data = yaml.load(raw)
    newPrices = {"provider/other": {"input": 3.0e-7, "output": 4.0e-7}}

    updated = updateModelPricing(data, newPrices)
    assert len(updated) == 0


def testUpdateModelPricingPartialUpdate():
    yaml = YAML()
    raw = (
        "model_list:\n"
        "  - model_name: priced-model\n"
        "    litellm_params:\n"
        "       model: provider/test\n"
        "    model_info:\n"
        "       input_cost_per_token: 1.0e-7\n"
        "       output_cost_per_token: 2.0e-7\n"
    )
    data = yaml.load(raw)
    newPrices = {"provider/test": {"input": 3.0e-7}}

    updated = updateModelPricing(data, newPrices)

    assert len(updated) == 1
    assert updated[0]["newInput"] == 3.0e-7
    assert updated[0]["newOutput"] == 2.0e-7  # unchanged
    assert data["model_list"][0]["model_info"]["output_cost_per_token"] == 2.0e-7
