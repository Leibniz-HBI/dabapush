from pathlib import Path
from dabapush.reader import read

def test_read():
    gen = [
        Path('./test_case_1/test_case_1.json')
    ]
    i = 0
    for path in read('./stubs/test_case_1/', pattern='json'):
        _gen = gen[i]
        i += 1
        assert  path == _gen