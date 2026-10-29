from src import dataLoader
from src import analyzer

def setup_module():
    dataLoader.loadDataStuff()

def testFindBuildingsByKanton():
    res = analyzer.findBuildingsByKanton('BS')
    assert len(res) > 0

def testCountByGebaeudekategorie():
    c = analyzer.countByGebaeudekategorie('1020')
    assert c >= 0

def testAverageGebaeudeflaeche():
    avg = analyzer.averageGebaeudeflaeche()
    assert avg > 0

def testAverageGebaeudevolumen():
    avg = analyzer.averageGebaeudevolumen()
    assert avg > 0

def testBuildingsOlderThan():
    old = analyzer.buildingsOlderThan(1950)
    assert isinstance(old, list)

def testBuildingsBuiltBetween():
    res = analyzer.buildingsBuiltBetween(2000, 2010)
    assert isinstance(res, list)

def testCountByHeatingSource():
    h = analyzer.countByHeatingSource()
    assert isinstance(h, dict)
    assert len(h) > 0

def testFilterByArea():
    res = analyzer.filterByArea(0, 100)
    assert isinstance(res, list)

def testGetBuildingsWithSolar():
    res = analyzer.getBuildingsWithSolar()
    assert isinstance(res, list)
