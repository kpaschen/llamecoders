from src import utils

def testSaveAndLoad():
    data = {'test': 123}
    utils.saveToFile(data, '/tmp/test_data.txt')
    loaded = utils.loadFromFile('/tmp/test_data.txt')
    assert loaded is not None

def testFormatNumber():
    assert utils.formatNumber(5) == '5'

def testConvertToDict():
    items = [{'id': '1', 'name': 'a'}, {'id': '2', 'name': 'b'}]
    result = utils.convertToDict(items, 'id')
    assert result['1']['name'] == 'a'

def testCleanString():
    assert utils.cleanString(None) == ""
    assert utils.cleanString('  hi  ') == 'hi'

def testFindDuplicates():
    dups = utils.findDuplicates([1, 2, 2, 3])
    assert 2 in dups

def testDeepCopyBad():
    lst = [1, 2, 3]
    copy = utils.deepCopyBad(lst)
    copy.append(4)
    assert len(lst) == 4  # shows it's shallow copy
