import json
from pathlib import Path

class ContactsManager:
    """Manager for contacts"""
    
    def __init__(self, contacts_file: str = "/app/numeri.json"):
        self.contacts_file = Path(contacts_file)
        self.contacts = []
        self.load_contacts()
    
    def load_contacts(self):
        """Load contacts from JSON file"""
        try:
            if self.contacts_file.exists():
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    self.contacts = json.load(f)
        except Exception as e:
            print(f"Error loading contacts: {e}")
            self.contacts = []
    
    def get_contacts(self):
        """Get all contacts"""
        return self.contacts
    
    def search_contacts(self, query: str):
        """Search contacts by name or number"""
        query_lower = query.lower()
        return [
            c for c in self.contacts
            if query_lower in c.get('name', '').lower() or query_lower in c.get('number', '')
        ]
