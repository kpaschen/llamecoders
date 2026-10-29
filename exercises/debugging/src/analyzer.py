# analyzer.py - does all the analysis in one place, badly
try:
    from src import dataLoader
except ImportError:
    import dataLoader
import math

# more globals
lastResult = None
tempStorage = []

def findBuildingsByKanton(kanton, data=None):
    if data == None:
        data = dataLoader.getAllData()
    res = []
    for b in data:
        k = b.get('Kanton')
        if k == kanton:  # case sensitive bug
            res.append(b)
    global lastResult
    lastResult = res
    return res

def countByGebaeudekategorie(code, data=None):
    if data == None:
        data = dataLoader.getAllData()
    c = 0
    for b in data:
        if b.get('Gebäudekategorie Code') == code:
            c = c + 1
    return c

def averageGebaeudeflaeche(data=None):
    if data == None:
        data = dataLoader.getAllData()
    total = 0
    count = 0
    for b in data:
        area = b.get('Geb\u00e4udefl\u00e4che (in m2)') or b.get('Gebäudevolumen (in m3)')  # wrong key
        # try correct key
        area = b.get('Geb\u00c3\u00a4udefl\u00c3\u00a4che (in m2)')
        if area == None:
            # try other variations
            for k,v in b.items():
                if 'Fl' in k and 'm2' in k:
                    area = v
                    break
        if area != '' and area != None:
            try:
                total = total + float(area)
                count = count + 1
            except:
                pass  # silently ignore bad data
    # BUG: division by zero
    avg = total / count
    return avg

def averageGebaeudevolumen(data=None):
    if data == None:
        data = dataLoader.getAllData()
    total = 0
    count = 0
    for b in data:
        vol = b.get('Geb\u00e4udevolumen (in m3)') or b.get('Gebäudevolumen (in m3)') or b.get('GebÃ¤udevolumen (in m3)')
        if vol != '' and vol != None:
            try:
                total = total + float(vol)
                count = count + 1
            except:
                pass
    # BUG: division by zero
    result = total / count
    return result

def buildingsOlderThan(year, data=None):
    if data == None:
        data = dataLoader.getAllData()
    res = []
    for b in data:
        bj = b.get('Baujahr des Gebäudes')
        if bj != '' and bj != None:
            try:
                if int(bj) < year:  # off by one? depends
                    res.append(b)
            except ValueError:
                continue  # skip
    return res

def buildingsBuiltBetween(year1, year2, data=None):
    if data == None:
        data = dataLoader.getAllData()
    res = []
    for b in data:
        bj = b.get('Baujahr des Gebäudes')
        if bj != '' and bj != None:
            try:
                y = int(bj)
                # BUG: off by one - excludes year2?
                if y >= year1 and y <= year2:
                    res.append(b)
            except:
                pass
    return res

def countByHeatingSource(data=None):
    if data == None:
        data = dataLoader.getAllData()
    result = {}
    for b in data:
        h = b.get('Primäre Energiequelle der Heizung Bezeichnung')
        if h == '':
            h = 'Unbekannt'
        # BUG: if key doesn't exist, will fail on increment in some cases? no wait - we check
        if h in result:
            result[h] = result[h] + 1
        else:
            result[h] = 1
    return result

def filterByArea(minA, maxA, data=None):
    if data == None:
        data = dataLoader.getAllData()
    res = []
    for b in data:
        a = b.get('Geb\u00e4udefl\u00e4che (in m2)') or b.get('Gebäudefläche (in m2)')
        if a != '' and a != None:
            try:
                area = float(a)
                # BUG: off by one - wrong bounds
                if area >= minA and area <= maxA:
                    res.append(b)
            except:
                pass
    return res

def getBuildingsWithSolar(data=None):
    if data == None:
        data = dataLoader.getAllData()
    res = []
    for b in data:
        # check warm water solar
        ww = b.get('Primärer Wärmeerzeuger Warmwasser Bezeichnung')
        if 'Solar' in str(ww):  # might miss case variations
            res.append(b)
        else:
            # also check secondary?
            pass
    return res

def complexAnalysis(x=[]):  # BUG: mutable default argument
    global tempStorage
    tempStorage = x
    # do something bad
    for i in range(len(tempStorage)):
        tempStorage.append(tempStorage[i])  # BUG: modifying list while iterating conceptually - grows forever
    return len(tempStorage)

def calculateEnergyScore(building):
    # nonsense calculation
    score = 0
    try:
        area = float(building.get('Gebäudefläche (in m2)', 0))
        vol = float(building.get('Gebäudevolumen (in m3)', 0))
        score = area * 0.5 + vol * 0.1
        # BUG: division issues
        if building.get('Anzahl Wohnungen') != '':
            score = score / int(building.get('Anzahl Wohnungen'))
        else:
            score = score / 0  # division by zero
    except:
        score = -1
    return score
