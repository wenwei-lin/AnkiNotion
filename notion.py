from email import header
from urllib import response
import requests
import json

class AnkiNotionClient:
    def __init__(self, key, database_id) -> None:
        self.key = key
        self.database_id = database_id
        self.headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
    
    def get_not_added_records(self):
        endpoint = f'https://api.notion.com/v1/databases/{self.database_id}/query'
        payload = {
            "page_size": 500,
            "filter": {
                "and": [
                    {
                            "property": 'Added',
                            'checkbox': {
                                'equals': False
                            }
                    }
                ]
            }
            
        }
        response = requests.post(endpoint, headers=self.headers, json=payload).json()
        return [(item['id'], item['properties']) for item in response['results']]
    
    def build_one_record_object(self, record):
        page_id = record['id']
        properties = []
        for property in record['properties']:
            



        
    
notion = AnkiNotionClient('secret_LGStXmKHRffm42pRFAcS86wadkih7I6vxnDmQwW7eVw', 'dd9b587a2fc74a55a4b3a81cc019fa48')
print(len(notion.get_not_added_records()))