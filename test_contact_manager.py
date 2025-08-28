import unittest
import os
import json
from contact_manager import ContactManager

class TestContactManager(unittest.TestCase):

    def setUp(self):
        """Set up a fresh contact manager before each test."""
        self.cm = ContactManager()
        self.test_file = "test_contacts.json"

    def tearDown(self):
        """Remove test files after tests run."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_contact(self):
        self.cm.add("Alice", "12345")
        self.assertEqual(len(self.cm.contact_list), 1)
        self.assertEqual(self.cm.contact_list[0]["name"], "Alice")

    def test_add_duplicate_contact(self):
        self.cm.add("Alice", "12345")
        self.cm.add("Alice", "67890")
        self.assertEqual(len(self.cm.contact_list), 1)

    def test_edit_contact(self):
        self.cm.add("Alice", "12345")
        self.cm.edit("Alice", new_number="54321")
        self.assertEqual(self.cm.contact_list[0]["number"], "54321")

    def test_edit_nonexistent_contact(self):
        self.cm.edit("Bob", new_number="11111")
        self.assertEqual(len(self.cm.contact_list), 0)

    def test_search_contact(self):
        self.cm.add("Alice", "12345")
        self.cm.add("Bob", "67890")
        results = self.cm.search("ali")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice")

    def test_backup_and_load(self):
        self.cm.add("Alice", "12345")
        self.cm.backup(self.test_file)

        # Load from saved file
        cm2 = ContactManager(self.test_file)
        self.assertEqual(len(cm2.contact_list), 1)
        self.assertEqual(cm2.contact_list[0]["name"], "Alice")

if __name__ == "__main__":
    unittest.main()
