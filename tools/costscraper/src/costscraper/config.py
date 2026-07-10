"""Config utilities for loading and saving litellm-config.yaml."""

from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarfloat import ScalarFloat


def _representFloat(representer, data):
    value = float(data)
    formatted = format(value, ".12f")
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    if formatted == "-0":
        formatted = "0"
    return representer.represent_scalar("tag:yaml.org,2002:float", formatted)


def createYamlRoundTrip():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.representer.add_representer(float, _representFloat)
    yaml.representer.add_representer(ScalarFloat, _representFloat)
    return yaml


def loadConfig(configPath):
    yaml = createYamlRoundTrip()
    with open(configPath, "r", encoding="utf-8") as f:
        return yaml.load(f)


def saveConfig(configPath, data):
    yaml = createYamlRoundTrip()
    with open(configPath, "w", encoding="utf-8") as f:
        yaml.dump(data, f)


def findModelsWithPricing(configData):
    models = []
    modelList = configData.get("model_list", [])
    for entry in modelList:
        modelInfo = entry.get("model_info", {})
        if (
            "input_cost_per_token" in modelInfo
            and "output_cost_per_token" in modelInfo
        ):
            models.append(
                {
                    "modelName": entry.get("model_name", ""),
                    "modelId": entry.get("litellm_params", {}).get("model", ""),
                    "inputCost": modelInfo["input_cost_per_token"],
                    "outputCost": modelInfo["output_cost_per_token"],
                    "entry": entry,
                }
            )
    return models


def updateModelPricing(configData, newPrices, dryRun=False):
    updated = []
    modelList = configData.get("model_list", [])
    for entry in modelList:
        modelInfo = entry.get("model_info", {})
        if (
            "input_cost_per_token" not in modelInfo
            or "output_cost_per_token" not in modelInfo
        ):
            continue

        modelId = entry.get("litellm_params", {}).get("model", "")
        if modelId not in newPrices:
            continue

        priceInfo = newPrices[modelId]
        oldInput = modelInfo["input_cost_per_token"]
        oldOutput = modelInfo["output_cost_per_token"]
        newInput = priceInfo.get("input")
        newOutput = priceInfo.get("output")

        changed = False
        if newInput is not None and newInput != oldInput:
            if not dryRun:
                modelInfo["input_cost_per_token"] = newInput
            changed = True
        if newOutput is not None and newOutput != oldOutput:
            if not dryRun:
                modelInfo["output_cost_per_token"] = newOutput
            changed = True

        if changed:
            updated.append(
                {
                    "modelName": entry.get("model_name", ""),
                    "modelId": modelId,
                    "oldInput": oldInput,
                    "oldOutput": oldOutput,
                    "newInput": newInput if newInput is not None else oldInput,
                    "newOutput": newOutput if newOutput is not None else oldOutput,
                }
            )

    return updated
