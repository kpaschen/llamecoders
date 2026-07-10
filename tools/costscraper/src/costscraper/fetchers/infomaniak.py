"""Infomaniak pricing fetcher."""

import requests
from bs4 import BeautifulSoup

from .base import Fetcher


class InfomaniakFetcher(Fetcher):
    """Scrape Infomaniak AI services pricing page for per-token costs."""

    url = "https://www.infomaniak.com/en/hosting/ai-services/prices"
    exchangeRateUrl = "https://api.exchangerate-api.com/v4/latest/CHF"

    def __init__(self, mapper=None, session=None):
        self.mapper = mapper
        self.session = session or requests.Session()

    def _fetchExchangeRate(self):
        response = self.session.get(self.exchangeRateUrl, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["rates"]["USD"]

    def fetchPrices(self):
        rate = self._fetchExchangeRate()
        response = self.session.get(self.url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return self._parsePrices(soup, rate)

    def _parsePrices(self, soup, rate):
        prices = {}
        content = soup.find(
            "div",
            class_=lambda x: x
            and "PricesSection-module--sectionWrapperPricesContent--" in x,
        )
        if not content:
            return prices

        for modelBlock in content.find_all("div", recursive=False):
            modelName = self._extractModelName(modelBlock)
            if not modelName:
                continue

            priceData = self._extractPriceData(modelBlock, rate)
            if not priceData:
                continue

            normalizedName = (
                self.mapper.normalizeName("infomaniak", modelName)
                if self.mapper
                else modelName
            )
            prices[normalizedName] = priceData

        return prices

    def _extractModelName(self, modelBlock):
        nameTag = modelBlock.find(
            "p",
            class_=lambda x: x and "IkTypography-module--h4--" in x,
        )
        if not nameTag:
            return None
        return nameTag.get_text(strip=True)

    def _extractPriceData(self, modelBlock, rate):
        priceDiv = modelBlock.find(
            "div",
            class_=lambda x: x
            and "PricesSection-module--sectionWrapperPricesContentModelsPrice--" in x,
        )
        if not priceDiv:
            return None

        priceData = {"input": None, "output": None}

        for row in priceDiv.find_all(
            "div",
            class_=lambda x: x
            and "PricesSection-module--sectionWrapperPricesContentModelsPriceWrapper--"
            in x,
        ):
            descTag = row.find(
                "p",
                class_=lambda x: x
                and "PricesSection-module--sectionWrapperPricesContentModelsPriceWrapperDesc--"
                in x,
            )
            if not descTag:
                continue

            desc = descTag.get_text(strip=True).lower()
            if "incoming" not in desc and "outgoing" not in desc:
                continue

            amountTag = row.find(
                "span",
                class_=lambda x: x and "IkTypography-module--h3--" in x,
            )
            if not amountTag:
                continue

            amountText = amountTag.get_text(strip=True)
            try:
                amount = float(amountText.replace(",", ".").replace("'", ""))
            except ValueError:
                continue

            suffixTag = row.find("span", class_="PricesSection-module--suffix--0de58")
            suffix = suffixTag.get_text(strip=True).lower() if suffixTag else ""

            multiplier = self._parseMultiplier(suffix)
            if multiplier is None:
                continue

            perTokenCost = (amount / multiplier) * rate

            if "incoming" in desc:
                priceData["input"] = perTokenCost
            elif "outgoing" in desc:
                priceData["output"] = perTokenCost

        return priceData if (priceData["input"] is not None or priceData["output"] is not None) else None

    def _parseMultiplier(self, suffix):
        suffixNormalized = suffix.replace(" ", "").lower()
        if "/1mtokens" in suffixNormalized or "/1mtoken" in suffixNormalized:
            return 1_000_000.0
        if "/10ktokens" in suffixNormalized or "/10ktoken" in suffixNormalized:
            return 10_000.0
        if "/100ktokens" in suffixNormalized or "/100ktoken" in suffixNormalized:
            return 100_000.0
        if "/1tokens" in suffixNormalized or "/1token" in suffixNormalized:
            return 1.0
        return None
