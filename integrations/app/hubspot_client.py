import os
import requests
from dotenv import load_dotenv

load_dotenv()

class HubSpotClient:
    def __init__(self):
        self.access_token = os.getenv('HUBSPOT_ACCESS_TOKEN')
        self.base_url = 'https://api.hubapi.com'
        
        if not self.access_token or self.access_token == 'your_private_app_access_token_here':
            raise ValueError('HUBSPOT_ACCESS_TOKEN not configured. Check your .env file.')
    
    def _get_headers(self):
        """Returns authorization headers with Bearer token"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self):
        """Test if the access token is valid"""
        try:
            response = requests.get(
                f'{self.base_url}/integrations/v1/me',
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Connection failed: {e}')
            return None
    
    def get_contacts(self, limit=10):
        """Fetch contacts from HubSpot CRM"""
        try:
            response = requests.get(
                f'{self.base_url}/crm/v3/objects/contacts',
                headers=self._get_headers(),
                params={'limit': limit}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Failed to fetch contacts: {e}')
            return None
    
    def create_contact(self, properties):
        """Create a new contact in HubSpot"""
        try:
            response = requests.post(
                f'{self.base_url}/crm/v3/objects/contacts',
                headers=self._get_headers(),
                json={'properties': properties}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Failed to create contact: {e}')
            return None
    
    def get_deals(self, limit=10):
        """Fetch deals from HubSpot CRM"""
        try:
            response = requests.get(
                f'{self.base_url}/crm/v3/objects/deals',
                headers=self._get_headers(),
                params={'limit': limit}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Failed to fetch deals: {e}')
            return None

if __name__ == '__main__':
    client = HubSpotClient()
    print('Testing HubSpot connection...')
    me = client.test_connection()
    if me:
        print(f'Connected! Portal: {me.get("portalId")}')
