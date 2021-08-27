import json
from pathlib import Path
from dabapush.read import read

def test_read():
    testFile = Path('./test_case_1/test_case_1.json')
    testFile.resolve()
    gen = [
        testFile    
    ]

    for count, path in enumerate(read('./stubs/test_case_1/', pattern='json', recursive=True)):
        _gen = gen[count]
        assert  path == _gen