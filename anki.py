import requests
import json

class Anki:
    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
    
    def request(self, action, **params):
        return {'action': action, 'params': params, 'version': 6}

    def invoke(self, action, **params):
        requestJson = json.dumps(self.request(action, **params)).encode('utf-8')
        response = requests.post(self.endpoint, data=requestJson).json()
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']
    
    def get_vocabulary_notes_id(self):
        vocabulary_deck_id = '1660354139084'
        result = self.invoke('findNotes', query='deck:Vocabulary')
        return result

    def get_vocabulary_note(self, id):
        notes = [id]
        result = self.invoke('notesInfo', notes=notes)[0]['fields']
        return result
    
    def get_vocabulary_note(self, id):
        notes = [id]
        result = self.invoke('notesInfo', notes=notes)[0]['fields']
        return result
    
    def update_vocabulary_note(self, id, fields, audio=[]):
        self.invoke('updateNoteFields', note={'id': id, 'fields': fields, 'audio': audio})
    
