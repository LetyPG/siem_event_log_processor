# Test to validate the data generator functions

import unittest
from helpers.data_generator import (
    generate_siem_event,
    generate_siem_events_csv,
    generate_test_data_with_edge_cases,
    generate_demo_data
)


class TestDataGenerator(unittest.TestCase):
    # Test that a single event is generated with all required fields
    def test_generate_siem_event(self):
        event = generate_siem_event()
        
        # Check all required fields are present
        self.assertIn('datetime', event)
        self.assertIn('source_ip', event)
        self.assertIn('destination_ip', event)
        self.assertIn('port', event)
        self.assertIn('event_type', event)
        self.assertIn('priority', event)
        
        # Check priority is in valid range
        self.assertGreaterEqual(event['priority'], 1)
        self.assertLessEqual(event['priority'], 5)
        
        # Check port is an integer
        self.assertIsInstance(event['port'], int)

    # Test that generated events have priorities consistent with their type
    def test_priority_consistency(self):
        from src.basic_functions.assign_priority_by_event_type import assign_priority_by_event_type
        
        for _ in range(20):
            event = generate_siem_event()
            expected_priority = assign_priority_by_event_type(event['event_type'])
            self.assertEqual(event['priority'], expected_priority, 
                             f"Event type {event['event_type']} should have priority {expected_priority}")
    
    # Test that CSV format is correct
    def test_generate_siem_events_csv(self):
        csv_data = generate_siem_events_csv(count=5)
        
        # Check it's a string
        self.assertIsInstance(csv_data, str)
        
        # Check it has the right number of lines (5 events + newline)
        lines = csv_data.strip().split('\n')
        self.assertEqual(len(lines), 5)
        
        # Check each line has 6 comma-separated fields
        for line in lines:
            fields = line.split(',')
            self.assertEqual(len(fields), 6)

    # Test that edge cases are included when requested    
    def test_generate_siem_events_csv_with_edge_cases(self):
        csv_data = generate_siem_events_csv(count=3, include_edge_cases=True)
        
        lines = csv_data.strip().split('\n')
        
        # Should have 3 normal events + 2 edge cases
        self.assertEqual(len(lines), 5)
        
        # Check that edge cases are present
        self.assertIn('linea,invalida', csv_data)
        self.assertIn('notanumber', csv_data)
    
    # Test that test data includes edge cases
    def test_generate_test_data_with_edge_cases(self):
        test_data = generate_test_data_with_edge_cases()
        
        # Check it's a string
        self.assertIsInstance(test_data, str)
        
        # Check it contains edge cases
        self.assertIn('linea,invalida', test_data)
        self.assertIn('notanumber', test_data)
        
        # Check it has at least 3 valid events + 2 edge cases
        lines = test_data.strip().split('\n')
        self.assertGreaterEqual(len(lines), 5)
    
    # Test that demo data is generated correctly
    def test_generate_demo_data(self):
        demo_data = generate_demo_data(count=10)
        
        # Check it's a string
        self.assertIsInstance(demo_data, str)
        
        # Check it has the right number of lines
        lines = demo_data.strip().split('\n')
        self.assertEqual(len(lines), 10)
    
    # Test that different datetime formats are generated
    def test_different_datetime_formats(self):
        formats_found = set()
        
        for _ in range(20):
            event = generate_siem_event()
            datetime_str = event['datetime']
            
            # Identify format based on patterns
            if 'T' in datetime_str and datetime_str.endswith('Z'):
                formats_found.add('with_zulu')
            elif '+' in datetime_str or datetime_str.count('-') > 2:
                if '+' in datetime_str:
                    formats_found.add('with_plus_timezone')
                else:
                    formats_found.add('with_timezone_offset')
            else:
                formats_found.add('without_timezone')
        
        # Should have generated at least 2 different formats
        self.assertGreaterEqual(len(formats_found), 2)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
