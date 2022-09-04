import requests
import json

from property import PagePropertyParser


class NotionClient:
    def __init__(self, key) -> None:
        self.key = key
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    def get_database(self, database_id):
        """Get the database information by its id"""
        endpoint = f"https://api.notion.com/v1/databases/{database_id}"
        response = requests.get(endpoint, headers=self.headers).json()
        return response

    def get_database_records(self, database_id, filter=None):
        """Get the database records by its id
        Return: list of page objects
        """
        endpoint = f"https://api.notion.com/v1/databases/{database_id}/query"
        payload = {"page_size": 100, "filter": filter} if filter else {"page_size": 100}
        response = requests.post(endpoint, headers=self.headers, json=payload).json()

        # if the response contains next cursor, then we need to get the next page
        if "next_cursor" not in response:
            result = response["results"]
        else:
            result = response["results"]
            while response["next_cursor"]:
                payload["start_cursor"] = response["next_cursor"]
                response = requests.post(
                    endpoint, headers=self.headers, json=payload
                ).json()
                result += response["results"]
        return result

    def get_page_properties(self, page):
        """Get the page properties"""
        property_parser = PagePropertyParser()
        return property_parser.parse_properties(page["properties"])
