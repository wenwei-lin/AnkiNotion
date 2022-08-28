from anki import Anki
from dictionary import MerriamWebster
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv()

def main():
    with open('/etc/resolv.conf', 'r') as wsl_file:
        wsl_ip = wsl_file.readlines()[-1].split()[1]

    anki_endpoint = f'http://{wsl_ip}:8765' 
    anki = Anki(anki_endpoint)

    dictionary_api_key = os.getenv('DICTIONARY_API_KEY')
    merriam_webster = MerriamWebster(dictionary_api_key)

    
    # Get all notes in Vocabulary deck
    notes_id = anki.get_vocabulary_notes_id()
    
    # Traverse all notes in Vocabulary deck
    for note_id in notes_id:
        # Get note fields
        note = anki.get_vocabulary_note(note_id)
        
        # Add pronunciation to note fields if it doesn't exist
        if note['US soundmark']['value'] == '':
            word = note['Word']['value']
            data = merriam_webster.get_pronunciation(word)
            if data is None:
                print(f"Cannot find {word}'s pronunciation")
                continue

            soundmark = data['soundmark']
            audio_url = data['audio_url']
            audio_filename = data['audio_filename']
            
            # Download audio file
            audio_data = requests.get(audio_url).content
            base64_encoded = base64.b64encode(audio_data).decode('utf-8')
            
            anki.update_vocabulary_note(id=note_id, fields={'US soundmark': soundmark}, audio=[{'data': base64_encoded, 'filename': f'{audio_filename}.mp3', 'fields': ['US pronunciation']}])
            print(f"{word}'s pronunciation added")
        


main()