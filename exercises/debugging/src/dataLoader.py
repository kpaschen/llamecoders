# dataLoader.py - loads data badly
import csv
import os

# globals are cool
dataCache = []
FILE_NAME = "100230.csv"

def loadDataStuff(path = None):
    global dataCache
    dataCache = []
    if path == None:
        # try to find file in various places
        possiblePaths = [FILE_NAME, "./" + FILE_NAME, "../" + FILE_NAME, 
                        "/home/sven/Seafile/owncloud/code/agentic/analyzedata/" + FILE_NAME]
        for p in possiblePaths:
            if os.path.exists(p):
                path = p
                break
    if path == None or not os.path.exists(path):
        raise Exception("File not found!")
    
    # bad encoding choice
    f = open(path, 'r', encoding='latin-1')
    reader = csv.reader(f, delimiter=';')
    try:
        headers = next(reader)
    except:
        f.close()
        return 0
    for row in reader:
        rowDict = {}
        for i in range(0, len(headers)):
            if i < len(row):
                rowDict[headers[i]] = row[i]
            else:
                rowDict[headers[i]] = ''
        dataCache.append(rowDict)
    f.close()
    return len(dataCache)

def getAllData():
    return dataCache

def getDataByIndex(idx):
    # no bounds checking
    return dataCache[idx]

def clearData():
    global dataCache
    dataCache = []
    return True
