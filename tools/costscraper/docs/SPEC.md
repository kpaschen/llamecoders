# costscraper Specification

## 1. Overview

`costscraper` is a CLI tool that fetches current per-token pricing from LLM
providers and updates the `model_info` cost fields in a
`litellm-config.yaml` file.

## 2. Scope & Constraints

- **Only update existing priced models.** The tool scans
  `litellm-config.yaml` for entries that already possess
  `input_cost_per_token` / `output_cost_per_token` fields and updates
  *only* those values.
- **No new entries.** The tool will not add new models to the config or
  insert pricing into models that lack it.
- **Applicable to:** The three Infomaniak models currently in the config
  (`infomaniak-qwen3.5-122b`, `infomaniak-qwen3.5`, `infomaniak-kimi`).
  OpenAI models are skipped because they have no pricing fields today.
- **License-safe.** All code and dependencies must be Apache-2.0-compatible.

## 3. Provider Fetchers (Extensible Architecture)

- **Modular design.** Each provider is handled by a dedicated fetcher
  class/module adhering to a common interface (e.g.
  `fetchPrices()` → returns structured pricing data).
- **Initial provider: Infomaniak.** Fetcher scrapes
  `https://www.infomaniak.com/en/hosting/ai-services/prices` to extract
  model names and their input/output token prices. Infomaniak lists prices
  in CHF; LiteLLM expects USD, so the fetcher fetches a live CHF→USD
  exchange rate from a public API and converts all token costs before
  returning them.
- **Extensibility.** The architecture must allow adding new provider
  fetchers (e.g., OpenAI pricing page, Cohere API) without touching core
  update logic.

## 4. Name Mapping

A provider-specific mapping layer normalizes between:

- The `model` value in the LiteLLM config (e.g.
  `Qwen/Qwen3.5-122B-A10B-FP8`)
- The model name as it appears on the provider's pricing page.

Mappings are configurable/maintainable per-provider.

## 5. CLI Interface

- **Entry point:** `costscraper` (or `python -m costscraper`).
- **Arguments:**
  - `--config <path>` (required) — Path to the `litellm-config.yaml` to
    read and update.
  - `--dry-run` (optional) — Parse current prices, compute the delta,
    print the proposed changes to stdout, but **do not write** to the
    file.

## 6. Update Behavior

1. Load and parse the YAML via a round-trip parser (`ruamel.yaml`) to
   preserve comments, formatting, and ordering.
2. Identify all models with existing `input_cost_per_token` /
   `output_cost_per_token` fields.
3. For each supported provider, fetch current pricing.
4. Match models and compute new values.
5. All displayed and written prices are formatted in fixed decimal notation
   (e.g., `0.0000007`) rather than scientific notation.
6. If `--dry-run`, print the intended changes and exit with code `0`.
7. If not `--dry-run`, write the updated YAML back to `--config`.

## 7. Error Handling

- **Unreachable provider page or exchange-rate API:** Print a warning
  message to stderr, leave existing values untouched, and continue
  processing other providers/models.
- **Parsing failure / missing model on pricing page:** Print a warning,
  skip that specific model, and continue.
- **No failures shall corrupt the original `litellm-config.yaml`.**

## 8. Technical Stack & Conventions

- **Language:** Python 3
- **Package manager:** `uv`
- **Structure:** Source in `src/`, tests in `tests/`
- **Naming:** camelCase for functions, classes, and variables (per
  `AGENTS.md`)
- **YAML library:** `ruamel.yaml` for round-trip parsing (preserves
  comments)
- **HTTP / Scraping:** `requests` + `beautifulsoup4` (or similar
  lightweight scraper)
- **Testing:** Maintain ≥70 % coverage.

## 9. Initial File Structure

```
costscraper/
├── src/
│   └── costscraper/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py         # YAML reading/writing, round-trip
│       ├── fetchers/
│       │   ├── __init__.py
│       │   ├── base.py       # Abstract fetcher interface
│       │   └── infomaniak.py # Infomaniak pricing scraper
│       └── mapping.py        # Model name normalization
├── tests/
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_infomaniak_fetcher.py
│   └── fixtures/
│       └── sample-litellm-config.yaml
├── docs/
│   └── SPEC.md
├── pyproject.toml
└── AGENTS.md
```
