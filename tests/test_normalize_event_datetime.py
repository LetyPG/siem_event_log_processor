# Test to validate the "normalize_event_datetime" function that converts the datetime format to UTC

import unittest
from helpers.test import TestEventSiemLogProcessor
from src.basic_functions.normalize_event_datetime import normalize_event_datetime


class TestNormalizeEventDatetime(TestEventSiemLogProcessor):
    def test_normalize_event_datetime(self):
        # Case 1> with timezone offset -0400
        event1 = {'datetime': '2024/09/01 14:23:01-0400'}
        normalized1 = normalize_event_datetime(event1)
        self.assertEqual(normalized1['datetime'], '2024-09-01 18:23:01')
        
        # Case 2: with timezone offset (Zulu/UTC)
        event2 = {'datetime': '2024-09-01T14:25:37Z'}
        normalized2 = normalize_event_datetime(event2)
        self.assertEqual(normalized2['datetime'], '2024-09-01 14:25:37')

        # Case 3: Without timezone , it should assume UTC
        event3 = {'datetime': '2024-09-01 15:00:15'}
        normalized3 = normalize_event_datetime(event3)
        self.assertEqual(normalized3['datetime'], '2024-09-01 15:00:15')

        # Case 4: with invalid format date
        event4 = {'datetime': 'not-a-date'}
        normalized4 = normalize_event_datetime(event4)
        self.assertEqual(normalized4['datetime'], 'Unknown Format')

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)