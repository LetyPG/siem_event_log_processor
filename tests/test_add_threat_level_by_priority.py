# Test to validate the "add_threat_level_by_priority" function that assigns a threat level based on the specified security priority.

import unittest
from helpers.test import TestEventSiemLogProcessor
from src.basic_functions.add_threat_level_by_priority import add_threat_level_by_priority


class TestAddThreatLevelByPriority(TestEventSiemLogProcessor):
    def test_add_threat_level_by_priority(self):
        event_low = {'priority': 2}
        event_medium = {'priority': 4}
        event_high = {'priority': 5}
        event_unknown = {'priority': 99}

        self.assertEqual(add_threat_level_by_priority(event_low)['threat_level'], 'Low')
        self.assertEqual(add_threat_level_by_priority(event_medium)['threat_level'], 'Medium')
        self.assertEqual(add_threat_level_by_priority(event_high)['threat_level'], 'High')
        self.assertEqual(add_threat_level_by_priority(event_unknown)['threat_level'], 'Unknown')

    def test_add_threat_level_with_event_type(self):
        """Test that priority is updated based on event type"""
        # Event with low priority but High threat event type
        event_conflict = {'priority': 1, 'event_type': 'DATA_EXFILTRATION'}
        
        processed_event = add_threat_level_by_priority(event_conflict)
        
        # Should be updated to priority 5 (High)
        self.assertEqual(processed_event['priority'], 5)
        self.assertEqual(processed_event['threat_level'], 'High')
        
        # Event with unknown type should keep original priority
        event_unknown = {'priority': 2, 'event_type': 'UNKNOWN_TYPE'}
        processed_event_unknown = add_threat_level_by_priority(event_unknown)
        self.assertEqual(processed_event_unknown['priority'], 2)
        self.assertEqual(processed_event_unknown['threat_level'], 'Low')
   
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)