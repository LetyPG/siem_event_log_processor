# Test to validate the "read_events_from_file" function that reads and  parsing the events from a file 

import unittest
from helpers.test import TestEventSiemLogProcessor
from src.basic_functions.read_events_from_file import read_events_from_file


class TestReadEventsFromFile(TestEventSiemLogProcessor):
    def test_read_events_from_file(self):
        events = read_events_from_file(self.test_file_path)
        
        # Should have 3 valid events (edge cases are filtered out)
        self.assertEqual(len(events), 3)
        
        # Check that all events have the required fields
        for event in events:
            self.assertIn('source_ip', event)
            self.assertIn('destination_ip', event)
            self.assertIn('port', event)
            self.assertIn('event_type', event)
            self.assertIn('priority', event)
            self.assertIn('datetime', event)
            
            # Check that priority is an integer in valid range
            self.assertIsInstance(event['priority'], int)
            self.assertGreaterEqual(event['priority'], 1)
            self.assertLessEqual(event['priority'], 5)
            
            # Check that port is an integer
            self.assertIsInstance(event['port'], int)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)