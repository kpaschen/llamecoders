# main.py - entry point, everything mixed together
import sys
import os

# try both import styles
try:
    from src import dataLoader
    from src import analyzer
    from src import utils
except ImportError:
    import dataLoader
    import analyzer
    import utils

# global state
CURRENT_FILE = None
RUN_COUNT = 0

def init():
    global CURRENT_FILE
    # hardcoded path
    CURRENT_FILE = "/home/sven/Seafile/owncloud/code/agentic/analyzedata/100230.csv"
    return dataLoader.loadDataStuff(CURRENT_FILE)

def doQuickAnalysis():
    global RUN_COUNT
    RUN_COUNT = RUN_COUNT + 1
    data = dataLoader.getAllData()
    if len(data) == 0:
        init()
        data = dataLoader.getAllData()
    print("Total: " + str(len(data)))
    avg = analyzer.averageGebaeudeflaeche()
    print("Avg Area: " + str(avg))
    avgv = analyzer.averageGebaeudevolumen()
    print("Avg Vol: " + str(avgv))
    heating = analyzer.countByHeatingSource()
    for k in heating:
        print(k + " -> " + str(heating[k]))
    return True

def searchAndReport(kantonName):
    # case sensitive issue
    res = analyzer.findBuildingsByKanton(kantonName)
    print("Found " + str(len(res)) + " buildings in " + kantonName)
    # do something inefficient
    totalArea = 0
    for r in res:
        a = r.get('Geb\u00e4udefl\u00e4che (in m2)')
        if a != '':
            totalArea = totalArea + float(a)
    print("Total area: " + str(totalArea))
    return res

def brokenFunction():
    # this function does nothing useful and has bugs
    x = []
    for i in range(10):
        x.append(i)
    # modifying while iterating in a bad way
    for item in x:
        x.remove(item)  # BUG: modifying list while iterating
    return x

def runEverything():
    init()
    doQuickAnalysis()
    searchAndReport('BS')  # hardcoded
    old = analyzer.buildingsOlderThan(1900)
    print("Very old buildings: " + str(len(old)))
    # call broken stuff
    brokenFunction()
    return "done"

if __name__ == '__main__':
    runEverything()
