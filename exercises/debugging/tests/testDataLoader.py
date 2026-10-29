import os
from src import dataLoader

def testLoadData():
    # try to load
    count = dataLoader.loadDataStuff()
    assert count > 0
    assert len(dataLoader.getAllData()) == count

def testGetDataByIndex():
    dataLoader.loadDataStuff()
    data = dataLoader.getDataByIndex(0)
    assert isinstance(data, dict)
    assert 'Kanton' in data

def testClearData():
    dataLoader.loadDataStuff()
    dataLoader.clearData()
    assert len(dataLoader.getAllData()) == 0
