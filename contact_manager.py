"""
A simple contact management system in Python.

Features:
- Add contacts
- Search contacts
- Edit contact details
- Backup contacts to a file
"""

import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class ContactManager:
    def __init__(self, path: str = "") -> None:
        """Initialize the contact manager with an optional existing contact file."""
        self.contact_list = []

        if path and os.path.exists(path):
            try:
                logging.info("Loading previous contacts...")
                with open(path, "r", encoding="utf-8") as f:
                    self.contact_list = json.load(f)
                logging.info("Contacts LOADED.")
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Error loading contacts: {e}")
        else:
            logging.info("No previous contacts found or invalid path.")

    def validate_contact(self, name: str, number: str) -> bool:
        """Validate that the name and number are strings."""
        if not isinstance(name, str) or not isinstance(number, str):
            logging.error("Invalid input. Name and number must be strings.")
            return False
        return True

    def add(self, name: str, number: str) -> None:
        """Add a new contact, checking if the name already exists."""
        if any(item["name"].lower() == name.lower() for item in self.contact_list):
            logging.warning(f"Contact with name '{name}' already exists.")
        elif self.validate_contact(name, number):
            self.contact_list.append({"name": name.strip(), "number": number.strip()})
            logging.info(f"Contact {name} added.")

    def edit(self, name: str, new_name: str = None, new_number: str = None) -> None:
        """Edit the contact's name or number based on the provided name."""
        for item in self.contact_list:
            if item["name"].lower() == name.lower():
                if new_name:
                    item["name"] = new_name.strip()
                if new_number:
                    item["number"] = new_number.strip()
                logging.info(f"Contact '{name}' updated to Name: {item['name']}, Number: {item['number']}")
                return
        logging.warning(f"Contact with name '{name}' not found.")

    def search(self, name: str) -> list:
        """Search for contacts matching the given name."""
        return [item for item in self.contact_list if name.lower() in item["name"].lower()]

    def backup(self, path: str = "./contact_list.json") -> None:
        """Back up the contact list to the specified file path."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.contact_list, f, indent=4)
            logging.info(f"Contacts backed up to {path}")
        except IOError as e:
            logging.error(f"Error saving contacts: {e}")

    def print(self) -> None:
        """Print all contacts in a readable format."""
        if self.contact_list:
            logging.info("Your contacts are:")
            for contact in self.contact_list:
                logging.info(f"Name: {contact['name']}, Number: {contact['number']}")
        else:
            logging.info("No contacts available.")
