import requests
import json


class AnkiClient:
    def __init__(self, endpoint="localhost:9876"):
        self.endpoint = endpoint

    def request(self, action, **params):
        return {"action": action, "params": params, "version": 6}

    def invoke(self, action, **params):
        requestJson = json.dumps(self.request(action, **params)).encode("utf-8")
        response = requests.post(self.endpoint, data=requestJson).json()
        if len(response) != 2:
            raise Exception("response has an unexpected number of fields")
        if "error" not in response:
            raise Exception("response is missing required error field")
        if "result" not in response:
            raise Exception("response is missing required result field")
        if response["error"] is not None:
            raise Exception(response["error"])
        return response["result"]

    def get_deck_names(self):
        """Returns a list of deck names."""
        result = self.invoke("deckNames")
        return result

    def get_deck_names_and_id(self):
        """Returns a dictionary of deck names and id."""
        result = self.invoke("deckNamesAndIds")
        return result

    def create_deck(self, deck_name):
        """Create a new deck."""
        self.invoke("createDeck", deck=deck_name)

    def get_note_ids(self, deck_name):
        """Returns a list of note ids."""
        result = self.invoke("findNotes", query=f"deck:{deck_name}")
        return result

    def get_note_info(self, note_id:int):
        """Returns a dictionary of note info."""
        result = self.invoke("notesInfo", notes=[note_id])
        return result
    
    def create_note(self, deck_name, note_type, fields, tags=None, audio=None, video=None, picture=None):
        """Create a new note.
        Media files should be a list of media file paths, base64 data, or url, for example:
         "audio": [{
                "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                "filename": "yomichan_ねこ_猫.mp3",
                "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                "fields": [
                    "Front"
                ]
            }],
        """
        self.invoke("addNote", note={"deckName": deck_name, "modelName": note_type, "fields": fields, "options": {"allowDuplicate": False}, "tags": tags, "audio": audio, "video": video, "picture": picture})
    
    def update_note(self, note_id, fields, audio=None, video=None, picture=None):
        """Update a note."""
        self.invoke("updateNoteFields", note={"id": note_id, "fields": fields, "audio":audio, "video": video, "picture": picture})


if __name__ == "__main__":
    with open("/etc/resolv.conf", "r") as wsl_file:
        wsl_ip = wsl_file.readlines()[-1].split()[1]

    anki_endpoint = f"http://{wsl_ip}:8765"
    anki_client = AnkiClient(anki_endpoint)

    
    
