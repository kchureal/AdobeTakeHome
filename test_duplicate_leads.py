import unittest
from deduplicate import deduplicate_leads


class TestDeduplicateLeads(unittest.TestCase):
    def test_newest_date_preferred(self):  # Case 1: Test for preference of newest date
        leads = [
            {"_id": "1", "email": "test@example.com", "firstName": "John", "lastName": "Doe", "address": "123 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "1", "email": "test@example.com", "firstName": "John", "lastName": "Doe", "address": "456 St", "entryDate": "2023-01-02T00:00:00+00:00"}
        ]
        unique_leads, _ = deduplicate_leads(leads)
        self.assertEqual(len(unique_leads), 1)
        self.assertEqual(unique_leads[0]["address"], "456 St")

    def test_duplicate_id(self):  # Case 2: Test dedup for duplicate IDs
        leads = [
            {"_id": "1", "email": "test1@example.com", "firstName": "John", "lastName": "Doe", "address": "123 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "1", "email": "test2@example.com", "firstName": "Jane", "lastName": "Doe", "address": "456 St", "entryDate": "2023-01-01T00:00:00+00:00"}
        ]
        unique_leads, _ = deduplicate_leads(leads)
        self.assertEqual(len(unique_leads), 1)
        self.assertEqual(unique_leads[0]["email"], "test2@example.com")

    def test_duplicate_email(self):  # Case 3: Test dedup for duplicate emails
        leads = [
            {"_id": "1", "email": "test@example.com", "firstName": "John", "lastName": "Doe", "address": "123 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "2", "email": "test@example.com", "firstName": "Jane", "lastName": "Doe", "address": "456 St", "entryDate": "2023-01-01T00:00:00+00:00"}
        ]
        unique_leads, _ = deduplicate_leads(leads)
        self.assertEqual(len(unique_leads), 1)
        self.assertEqual(unique_leads[0]["_id"], "2")

    def test_same_date_prefer_last(self):  # Case 4 : Test that if dates are identical, preference of later date
        leads = [
            {"_id": "1", "email": "test@example.com", "firstName": "John", "lastName": "Doe", "address": "123 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "1", "email": "test@example.com", "firstName": "Jane", "lastName": "Doe", "address": "456 St", "entryDate": "2023-01-01T00:00:00+00:00"}
        ]
        unique_leads, _ = deduplicate_leads(leads)
        self.assertEqual(len(unique_leads), 1)
        self.assertEqual(unique_leads[0]["firstName"], "Jane")

    def test_no_duplicates(self):  # Case 5: No duplicates are removed if no exist
        leads = [
            {"_id": "1", "email": "test1@example.com", "firstName": "John", "lastName": "Doe", "address": "123 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "2", "email": "test2@example.com", "firstName": "Jane", "lastName": "Doe", "address": "456 St", "entryDate": "2023-01-01T00:00:00+00:00"}
        ]
        unique_leads, _ = deduplicate_leads(leads)
        self.assertEqual(len(unique_leads), 2)

    def test_multiple_duplicates(self):  # Case 6: Multiple duplicate scenario
        leads = [
            {"_id": "1", "email": "test@example.com", "firstName": "John", "lastName": "Doe", "address": "123 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "1", "email": "test@example.com", "firstName": "Jane", "lastName": "Doe", "address": "456 St", "entryDate": "2023-01-02T00:00:00+00:00"},
            {"_id": "2", "email": "test2@example.com", "firstName": "Alice", "lastName": "Smith", "address": "789 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "2", "email": "test2@example.com", "firstName": "Bob", "lastName": "Smith", "address": "101 St", "entryDate": "2023-01-03T00:00:00+00:00"}
        ]
        unique_leads, _ = deduplicate_leads(leads)
        self.assertEqual(len(unique_leads), 2)
        self.assertEqual(unique_leads[0]["firstName"], "Jane")
        self.assertEqual(unique_leads[1]["firstName"], "Bob")

    def test_change_log(self):  # Case 7: Test logging helper func
        leads = [
            {"_id": "1", "email": "test@example.com", "firstName": "John", "lastName": "Doe", "address": "123 St", "entryDate": "2023-01-01T00:00:00+00:00"},
            {"_id": "1", "email": "test@example.com", "firstName": "Jane", "lastName": "Doe", "address": "456 St", "entryDate": "2023-01-02T00:00:00+00:00"}
        ]
        _, change_log = deduplicate_leads(leads)
        self.assertEqual(len(change_log), 1)
        self.assertEqual(change_log[0]["changes"]["firstName"]["from"], "John")
        self.assertEqual(change_log[0]["changes"]["firstName"]["to"], "Jane")
        self.assertEqual(change_log[0]["changes"]["address"]["from"], "123 St")
        self.assertEqual(change_log[0]["changes"]["address"]["to"], "456 St")


if __name__ == "__main__":
    unittest.main()