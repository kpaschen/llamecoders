# utils.py - random utilities, badly organized
import os
import json

def saveToFile(data, filename):
    # writes without proper handling
    f = open(filename, 'w')
    f.write(str(data))
    f.close()
    return True

def loadFromFile(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    try:
        # try to parse as json
        return json.loads(content)
    except:
        return content

def formatNumber(num):
    # bad formatting
    return str(num)

def convertToDict(items, keyField):
    result = {}
    for i in range(len(items)):
        item = items[i]
        k = item.get(keyField)
        if k in result:  # if duplicate, overwrite silently - bad
            pass  # or should handle?
        result[k] = item
    return result

def cleanString(s):
    if s == None:
        return ""
    # bad cleaning
    return str(s).strip()

def findDuplicates(listOfThings):
    seen = []
    dups = []
    for item in listOfThings:
        if item in seen:
            dups.append(item)
        else:
            seen.append(item)
    return dups

def deepCopyBad(obj):
    # shallow copy disguised as deep copy
    if type(obj) == list:
        return obj[:]  # shallow
    if type(obj) == dict:
        return obj.copy()  # shallow
    return obj
