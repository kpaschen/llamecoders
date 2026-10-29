from src import main
from src import dataLoader

def testInit():
    res = main.init()
    assert res > 0

def testDoQuickAnalysis():
    main.init()
    res = main.doQuickAnalysis()
    assert res == True

def testSearchAndReport():
    main.init()
    res = main.searchAndReport('BS')
    assert isinstance(res, list)

def testBrokenFunction():
    res = main.brokenFunction()
    assert isinstance(res, list)

def testRunEverything():
    res = main.runEverything()
    assert res == 'done'
