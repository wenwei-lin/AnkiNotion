from anki import Anki
from dictionary import MerriamWebster
from dotenv import load_dotenv
from audio import AzureAudio
import os
import re
import requests
import base64

load_dotenv()

CLEANR = re.compile('<.*?>') 

def clean_html(raw_html):
  clean_text = re.sub(CLEANR, '', raw_html)
  return clean_text

def main():
    with open('/etc/resolv.conf', 'r') as wsl_file:
        wsl_ip = wsl_file.readlines()[-1].split()[1]

    anki_endpoint = f'http://{wsl_ip}:8765' 
    anki = Anki(anki_endpoint)

    dictionary_api_key = os.getenv('DICTIONARY_API_KEY')
    merriam_webster = MerriamWebster(dictionary_api_key)

    azure_audio = AzureAudio(os.getenv('AZURE_SPEECH_KEY'), os.getenv('AZURE_SPEECH_REGION'))

    
    # Get all notes in Vocabulary deck
    notes_id = anki.get_vocabulary_notes_id()
    
    # Traverse all notes in Vocabulary deck
    for note_id in notes_id:
        # Get note fields
        note = anki.get_vocabulary_note(note_id)
        
        
        # Add pronunciation to note fields if it doesn't exist
        if note['ContextSpeech']['value'] == '':
            word = note['Word']['value']
            context = clean_html(note['Context']['value'])
            audio_name = f'{note_id}{word}_context.wav'

            data = azure_audio.synthesize_audio(context)
            enc = base64.b64encode(data).decode('utf-8')
            # print(stream)

            anki.update_vocabulary_note(id=note_id, fields={}, audio=[{'data': enc, 'filename': f'{audio_name}', 'fields': ['ContextSpeech']}])

            # data = merriam_webster.get_pronunciation(word)
            # if data is None:
            #     print(f"Cannot find {word}'s pronunciation")
            #     continue

            # soundmark = data['soundmark']
            # audio_url = data['audio_url']
            # audio_filename = data['audio_filename']
            
            # # Download audio file
            # audio_data = requests.get(audio_url).content
            # base64_encoded = base64.b64encode(audio_data).decode('utf-8')
            
            # anki.update_vocabulary_note(id=note_id, fields={'US soundmark': soundmark}, audio=[{'data': base64_encoded, 'filename': f'{audio_filename}.mp3', 'fields': ['US pronunciation']}])
            # print(f"{word}'s pronunciation added")
            print(f"{word}'s context speech added")
            

main()