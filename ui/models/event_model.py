# Model layer for SIEM event data handling

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter


class EventModel:
    """Model for handling SIEM event data"""
    
    def __init__(self, data_file: str = "../processed_events.json"):
        """
        Initialize the event model.
        
        Args:
            data_file: Path to the JSON file containing processed events
        """
        self.data_file = data_file
    
    def load_processed_events(self) -> List[Dict[str, Any]]:
        """
        Load processed events from JSON file.
        
        Returns:
            List of event dictionaries
        """
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                events = json.load(f)
                return events if isinstance(events, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistics from processed events.
        
        Returns:
            Dictionary containing event statistics
        """
        events = self.load_processed_events()
        
        if not events:
            return {
                'total_events': 0,
                'high_threat': 0,
                'medium_threat': 0,
                'low_threat': 0,
                'unknown_threat': 0,
                'last_updated': None,
                'event_types': {}
            }
        
        # Count threat levels
        threat_counts = Counter(event.get('threat_level', 'Unknown') for event in events)
        
        # Count event types
        event_types = Counter(event.get('event_type', 'Unknown') for event in events)
        
        # Get most recent datetime
        datetimes = [event.get('datetime') for event in events if event.get('datetime')]
        last_updated = max(datetimes) if datetimes else None
        
        return {
            'total_events': len(events),
            'high_threat': threat_counts.get('High', 0),
            'medium_threat': threat_counts.get('Medium', 0),
            'low_threat': threat_counts.get('Low', 0),
            'unknown_threat': threat_counts.get('Unknown', 0),
            'last_updated': last_updated,
            'event_types': dict(event_types.most_common(5))
        }
    
    def filter_events(
        self,
        threat_level: Optional[str] = None,
        source_ip: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Filter events based on criteria.
        
        Args:
            threat_level: Filter by threat level (High, Medium, Low)
            source_ip: Filter by source IP address (partial match)
            event_type: Filter by event type
            limit: Maximum number of events to return
            
        Returns:
            Filtered list of events
        """
        events = self.load_processed_events()
        filtered = events
        
        # Apply filters
        if threat_level:
            filtered = [e for e in filtered if e.get('threat_level') == threat_level]
        
        if source_ip:
            filtered = [e for e in filtered if source_ip in e.get('source_ip', '')]
        
        if event_type:
            filtered = [e for e in filtered if e.get('event_type') == event_type]
        
        # Sort by datetime (most recent first) and limit
        filtered.sort(key=lambda x: x.get('datetime', ''), reverse=True)
        
        return filtered[:limit]
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent events.
        
        Args:
            limit: Number of events to return
            
        Returns:
            List of recent events
        """
        events = self.load_processed_events()
        events.sort(key=lambda x: x.get('datetime', ''), reverse=True)
        return events[:limit]
