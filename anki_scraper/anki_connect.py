import json
import urllib.request
from pathlib import Path

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# if __name__ == '__main__':
#     this_file = Path(__file__).resolve()
#     project_root = this_file.parents[1]  # adjust if your tree differs
#     path = project_root / "generated_decks" / "design_patterns.apkg"
#     invoke("importPackage", path = str(path))
#     invoke("sync")    