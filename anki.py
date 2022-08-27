from urllib import response
import requests
import json

with open('/etc/resolv.conf', 'r') as wsl_file:
    wsl_ip = wsl_file.readlines()[-1].split()[1]

endpoint = f'http://{wsl_ip}:8765'

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = requests.post(endpoint, data=requestJson).json()
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def get_vocabulary_notes_id():
    vocabulary_deck_id = '1660354139084'
    result = invoke('findNotes', query='deck:Vocabulary')
    print(result)

def get_vocabulary_note(id):
    notes = [id]
    result = invoke('notesInfo', notes=notes)[0]['fields']
    return result

def update_vocabulary_note(id, fields, audio):
    invoke('updateNoteFields', note={'id': id, 'fields': fields, audio: audio})

