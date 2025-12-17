# Add threat level to the event based on priority, include on the dictionary, using an scale of 1 to 5

from typing import Any, Dict 
import logging 
from src.basic_functions.assign_priority_by_event_type import assign_priority_by_event_type


THREAT_LEVEL_MAP = {
    (1, 2): "Low",
    (3, 4): "Medium",
    (5,): "High"
}

# First, try to assign/update priority based on event_type if it exists
def add_threat_level_by_priority(event: Dict[str, Any]) -> Dict[str, Any]:
    event_type = event.get('event_type')
    if event_type:
        new_priority = assign_priority_by_event_type(event_type)
        if new_priority > 0:
            event['priority'] = new_priority
            logging.info(f"[INFO]: Updated priority to {new_priority} based on event type '{event_type}'")

    # Then proceed with threat level assignment based on (possibly updated) priority
    priority = event.get('priority')                           
    threat_level = "Unknown"                                 
    if isinstance(priority, int):                               
        for priority_range, level in THREAT_LEVEL_MAP.items():  
            if priority in priority_range:                    
                threat_level = level
                break
    event['threat_level'] = threat_level                        
    logging.info(f"[INFO]: The threat level for the event is: {threat_level}")
    logging.debug(f"[DEBUG]: The type of priority is: {type(priority)}")   
    return event  
