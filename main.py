from dotenv import load_dotenv
from notion.client import NotionClient
import os
import re
import base64


def main():
    load_dotenv()
    notion = NotionClient(token_v2=os.getenv("NOTION_TOKEN"))
    
    
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