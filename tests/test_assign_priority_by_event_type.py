# Test to validate the "assign_priority_by_event_type" function

import unittest
from helpers.test import TestEventSiemLogProcessor
from src.basic_functions.assign_priority_by_event_type import assign_priority_by_event_type


class TestAssignPriorityByEventType(TestEventSiemLogProcessor):
    
    def test_assign_priority_known_types(self):
        """Test that known event types return the correct priority"""
        self.assertEqual(assign_priority_by_event_type('DATA_EXFILTRATION'), 5)
        self.assertEqual(assign_priority_by_event_type('SSH_BRUTE_FORCE'), 4)
        self.assertEqual(assign_priority_by_event_type('UNAUTHORIZED_ACCESS'), 3)
        self.assertEqual(assign_priority_by_event_type('LOGIN_FAILED'), 2)
        self.assertEqual(assign_priority_by_event_type('LOGIN_SUCCESS'), 1)

    def test_assign_priority_unknown_type(self):
        """Test that unknown event types return 0"""
        self.assertEqual(assign_priority_by_event_type('UNKNOWN_EVENT_TYPE'), 0)
        self.assertEqual(assign_priority_by_event_type(''), 0)

if __name__ == '__main__':
    unittest.main()
