from dotenv import load_dotenv
from notion.client import NotionClient
from anki.client import AnkiClient
from dictionary.merriam_webster import MerriamWebster
from cloud_service.speech import AzureSpeech
import os
import re
import base64
import requests
import uuid


def main():
    load_dotenv()
    with open('/etc/resolv.conf', 'r') as wsl_file:
        wsl_ip = wsl_file.readlines()[-1].split()[1]
    
    notion = NotionClient(token_v2=os.getenv("NOTION_TOKEN"))
    anki = AnkiClient(f"http://{wsl_ip}:8765")
    merria_webster = MerriamWebster(os.getenv("MERRIAM_WEBSTER_TOKEN"))
    azure_speech = AzureSpeech(key=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))

    
    # Fetch not added records from Notion Database
    database_id = os.getenv("NOTION_DATABASE_ID")
    record_pages = notion.get_database_records(database_id, filter={"and":[{"property":"Added","checkbox":{"equals":False}}, ]})

    for page in record_pages:
        # Get the page properties
        page_id = page['id']
        page_properties = notion.get_page_properties(page)
        # print(page_properties)
        

        # Fetch word's soundmark & audio
        word = page_properties["Word"]
        soundmark, pronunciation_audio_url = merria_webster.get_pronunciation(word)
        if soundmark is None: soundmark = ''

        if pronunciation_audio_url is not None:
            pronunciation_audio_data = requests.get(pronunciation_audio_url).content
            pronunciation_audio_base64 = base64.b64encode(pronunciation_audio_data).decode("utf-8")
            pronunciation_audio_filename = f"{word}-audio-{uuid.uuid4()}.mp3"
        else:
            pronunciation_audio_data = azure_speech.synthesize_audio(word)
            pronunciation_audio_base64 = base64.b64encode(pronunciation_audio_data).decode("utf-8")
            pronunciation_audio_filename = f"{word}-audio-{uuid.uuid4()}.wav"
        

        # Synthesize audio for context
        context = page_properties["Context"]
        context_audio_data = azure_speech.synthesize_audio(context)
        context_audio_base64 = base64.b64encode(context_audio_data).decode("utf-8")

        # Create new note in Anki
        resource = page_properties["Resource"]

        # Check if the deck exists
        deck_names = anki.get_deck_names()
        if f'Vocabulary::{resource}' not in deck_names:
            anki.create_deck(f'Vocabulary::{resource}')

        fields = {
            "Word": word,
            "Context": context.replace(word, '<span style="font-weight: 600; color: rgb(212, 76, 71);">{}</span>'.format(word)),
            "Meaning": page_properties["Meaning"],
            "Chinese": page_properties["Chinese"],
            "Soundmark": soundmark,
        }

        audio = [
            {
                "data": context_audio_base64,
                "filename": f"{word}-context-{uuid.uuid4()}.wav",
                "fields": ["Context Audio"],
            },
            {
                "data": pronunciation_audio_base64,
                "filename": pronunciation_audio_filename,
                "fields": ["Pronunciation Audio"],
            }
        ]

        anki.create_note(deck_name=f'Vocabulary::{resource}', modal_name="Vocabulary", fields=fields, audio=audio)

        # Update Notion
        notion.update_page_properties(page_id, {"Added": True})
        print(f"Added {word} to Anki")
        

if __name__ == "__main__":
    main()