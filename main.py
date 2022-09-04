from dotenv import load_dotenv
from notion.client import NotionClient
from anki.client import AnkiClient
from dictionary.merria_webster import MerriaWebster
from cloud_service.speech import AzureSpeech
import os
import re
import base64


def main():
    load_dotenv()
    with open('/etc/resolv.conf', 'r') as wsl_file:
        wsl_ip = wsl_file.readlines()[-1].split()[1]
    
    notion = NotionClient(token_v2=os.getenv("NOTION_TOKEN"))
    anki = AnkiClient(f"http://{wsl_ip}:8765")
    merria_webster = MerriaWebster(os.getenv("MERRIA_WEBSTER_TOKEN"))
    azure_speech = AzureSpeech(key=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))

    
    # Fetch not added records from Notion Database
    database_id = os.getenv("NOTION_DATABASE_ID")
    record_pages = notion.get_database_records(database_id, filter={"property": "Added", "checkbox": {"equals": False}})

    for page in record_pages:
        # Get the page properties
        page_properties = notion.get_page_properties(page)
        print(page_properties)
        break

        # Fetch word's soundmark & audio

        # Synthesize audio for context

        # Create new note in Anki


if __name__ == "__main__":
    main()