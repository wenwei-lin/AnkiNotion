from operator import contains
from notion.client import NotionClient
import os
import re
import json
from dotenv import load_dotenv


def main():
    load_dotenv()
    notion = NotionClient(token_v2=os.getenv("NOTION_TOKEN"))
    database_id = os.getenv("NOTION_DATABASE_ID")
    record_pages = notion.get_database_records(database_id, filter={"and":[{"property":"Added","checkbox":{"equals":False}}, {"property":"Word","title":{"is_not_empty":True}}, {"property":"Context","rich_text":{"is_empty":True}}]})
    print(len(record_pages))

    with open("notes.txt", "r") as f:
        contexts = f.read().splitlines()
        contexts = list(filter(None, contexts))

    for page in record_pages:
        print(page["id"])
        properties = notion.get_page_properties(page)
        word = properties["Word"].strip()
        print("Word: ", word)
        context = None
        for item in contexts:
            if item.find(word) != -1:
                context = item
                if not context.endswith("."):
                    context = context + '.'
                break
        
        print("Context: ", context)
        
        if context is not None:
            notion.update_page_properties(page["id"], {"Context": [{"type": "text", "text": {"content": context}}]})
        


if __name__ == '__main__':
    main()