import requests

class NotionClient:
    def __init__(self, key) -> None:
        self.key = key
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
    
    def get_database(self, database_id):
        """Get the database information by its id"""
        endpoint = f'https://api.notion.com/v1/databases/{database_id}'
        response = requests.get(endpoint, headers=self.headers).json()
        return response