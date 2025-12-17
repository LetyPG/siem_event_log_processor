# Test to validate the "combine_read_file_normalize_timestamp_add_threat_level" function which calls the previous functions (read_events_from_file, normalize_event_datetime, add_threat_level_by_priority).

import unittest
from helpers.test import TestEventSiemLogProcessor
from src.complex_processor_functions.combined_processor_functions import combine_read_file_normalize_timestamp_add_threat_level


class TestCombineReadFileNormalizeTimestampAddThreatLevel(TestEventSiemLogProcessor):
    def test_combine_read_file_normalize_timestamp_add_threat_level(self):
        processed_events = combine_read_file_normalize_timestamp_add_threat_level(self.test_file_path)
        
        # Verify the number of processed events (3 valid events)
        self.assertEqual(len(processed_events), 3)
        
        # Verify all events have required fields and correct threat levels
        for event in processed_events:
            # Check all required fields are present
            self.assertIn('datetime', event)
            self.assertIn('threat_level', event)
            self.assertIn('source_ip', event)
            self.assertIn('destination_ip', event)
            self.assertIn('port', event)
            self.assertIn('event_type', event)
            self.assertIn('priority', event)
            
            # Verify datetime is normalized (should be in UTC format: YYYY-MM-DD HH:MM:SS)
            self.assertRegex(event['datetime'], r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
            
            # Verify threat level matches priority
            priority = event['priority']
            threat_level = event['threat_level']
            if priority in [1, 2]:
                self.assertEqual(threat_level, 'Low')
            elif priority in [3, 4]:
                self.assertEqual(threat_level, 'Medium')
            elif priority == 5:
                self.assertEqual(threat_level, 'High')


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
