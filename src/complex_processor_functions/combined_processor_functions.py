# Combine functions to read, normalize, and enrich the events in a complex function.

from typing import Any, Dict, List 
import logging 
from src.basic_functions.read_events_from_file import read_events_from_file
from src.basic_functions.normalize_event_datetime import normalize_event_datetime
from src.basic_functions.add_threat_level_by_priority import add_threat_level_by_priority






def combine_read_file_normalize_timestamp_add_threat_level(
        file_path: str, max_events: int = 100000) -> List[Dict[str, Any]]:  
    raw_events = read_events_from_file(file_path)                           
    if not raw_events:                                                      
        print(f"[INFO] It was not found events in '{file_path}'.")
        return []

    if len(raw_events) > max_events:
        raise ValueError(f"[ERROR] The file contains {len(raw_events)} events. Limit allowed: {max_events}")      
    logging.info(f"[INFO] Processing {len(raw_events)} events from '{file_path}'...") 
    processed_events = [                                                         
        add_threat_level_by_priority(normalize_event_datetime(event)) 
        for event in raw_events
        if event.get('datetime') and event.get('source_ip') and event.get('destination_ip')
        and event.get('port') and event.get('event_type') and event.get('priority')
         ]
    
    return processed_events 
                                                   

    
   
