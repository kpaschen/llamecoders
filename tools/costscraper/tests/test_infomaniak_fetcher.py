"""Tests for Infomaniak fetcher."""

from pathlib import Path

from bs4 import BeautifulSoup

from costscraper.fetchers.infomaniak import InfomaniakFetcher
from costscraper.mapping import ModelMapper


fixtureHtml = Path(__file__).parent / "fixtures" / "infomaniak-pricing.html"


def makeFetcher(html=None):
    fetcher = InfomaniakFetcher()
    if html is not None:
        fetcher._html = html
    return fetcher


def testParseMultiplier1M():
    fetcher = InfomaniakFetcher()
    assert fetcher._parseMultiplier("/ 1M tokens") == 1_000_000.0
    assert fetcher._parseMultiplier("/1M tokens") == 1_000_000.0
    assert fetcher._parseMultiplier("/ 1M token") == 1_000_000.0


def testParseMultiplier10K():
    fetcher = InfomaniakFetcher()
    assert fetcher._parseMultiplier("/ 10K tokens") == 10_000.0
    assert fetcher._parseMultiplier("/10K tokens") == 10_000.0


def testParseMultiplierUnknown():
    fetcher = InfomaniakFetcher()
    assert fetcher._parseMultiplier("/ minute") is None


def testExtractModelName():
    fetcher = InfomaniakFetcher()
    html = (
        '<div>'
        '  <p class="color-text-primary fw-500 IkTypography-module--h4--7067e">'
        '    moonshotai/Kimi-K2.6'
        '  </p>'
        '</div>'
    )
    soup = BeautifulSoup(html, "html.parser")
    name = fetcher._extractModelName(soup.div)
    assert name == "moonshotai/Kimi-K2.6"


def testExtractModelNameMissing():
    fetcher = InfomaniakFetcher()
    html = "<div><p>other text</p></div>"
    soup = BeautifulSoup(html, "html.parser")
    name = fetcher._extractModelName(soup.div)
    assert name is None


def testExtractPriceData():
    fetcher = InfomaniakFetcher()
    html = (
        '<div>'
        '  <div class="PricesSection-module--sectionWrapperPricesContentModelsPrice--a729a">'
        '    <div class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapper--2caf3">'
        '      <p class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapperDesc--fbb2b">Incoming token:</p>'
        '      <span class="IkTypography-module--h3--4b530">0.60</span>'
        '      <span class="PricesSection-module--suffix--0de58">/ 1M tokens</span>'
        '    </div>'
        '    <div class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapper--2caf3">'
        '      <p class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapperDesc--fbb2b">Outgoing token:</p>'
        '      <span class="IkTypography-module--h3--4b530">3.00</span>'
        '      <span class="PricesSection-module--suffix--0de58">/ 1M tokens</span>'
        '    </div>'
        '  </div>'
        '</div>'
    )
    soup = BeautifulSoup(html, "html.parser")
    data = fetcher._extractPriceData(soup.div, rate=1.0)
    assert data is not None
    assert data["input"] == 0.60 / 1_000_000.0
    assert data["output"] == 3.00 / 1_000_000.0


def testExtractPriceDataWithConversion():
    fetcher = InfomaniakFetcher()
    html = (
        '<div>'
        '  <div class="PricesSection-module--sectionWrapperPricesContentModelsPrice--a729a">'
        '    <div class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapper--2caf3">'
        '      <p class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapperDesc--fbb2b">Incoming token:</p>'
        '      <span class="IkTypography-module--h3--4b530">0.60</span>'
        '      <span class="PricesSection-module--suffix--0de58">/ 1M tokens</span>'
        '    </div>'
        '  </div>'
        '</div>'
    )
    soup = BeautifulSoup(html, "html.parser")
    data = fetcher._extractPriceData(soup.div, rate=1.1)
    assert data is not None
    assert data["input"] == (0.60 / 1_000_000.0) * 1.1


def testExtractPriceDataPartial():
    fetcher = InfomaniakFetcher()
    html = (
        '<div>'
        '  <div class="PricesSection-module--sectionWrapperPricesContentModelsPrice--a729a">'
        '    <div class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapper--2caf3">'
        '      <p class="PricesSection-module--sectionWrapperPricesContentModelsPriceWrapperDesc--fbb2b">Incoming token:</p>'
        '      <span class="IkTypography-module--h3--4b530">1.20</span>'
        '      <span class="PricesSection-module--suffix--0de58">/ 1M tokens</span>'
        '    </div>'
        '  </div>'
        '</div>'
    )
    soup = BeautifulSoup(html, "html.parser")
    data = fetcher._extractPriceData(soup.div, rate=1.0)
    assert data is not None
    assert data["input"] == 1.20 / 1_000_000.0
    assert data["output"] is None


def testExtractPriceDataMissingPrice():
    fetcher = InfomaniakFetcher()
    html = "<div></div>"
    soup = BeautifulSoup(html, "html.parser")
    data = fetcher._extractPriceData(soup.div, rate=1.0)
    assert data is None


def testParsePricesFromFixture():
    fetcher = InfomaniakFetcher()
    text = fixtureHtml.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    prices = fetcher._parsePrices(soup, rate=1.0)

    assert "moonshotai/Kimi-K2.6" in prices
    assert "Qwen/Qwen3.5-122B-A10B-FP8" in prices
    assert "Qwen/Qwen3.5-397B-A17B-FP8" in prices

    assert prices["moonshotai/Kimi-K2.6"]["input"] == 0.60 / 1_000_000.0
    assert prices["moonshotai/Kimi-K2.6"]["output"] == 3.00 / 1_000_000.0


def testParsePricesWithMapper():
    mapper = ModelMapper({"infomaniak": {"moonshotai/Kimi-K2.6": "custom-kimi"}})
    fetcher = InfomaniakFetcher(mapper=mapper)
    text = fixtureHtml.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    prices = fetcher._parsePrices(soup, rate=1.0)

    assert "custom-kimi" in prices
    assert "moonshotai/Kimi-K2.6" not in prices
