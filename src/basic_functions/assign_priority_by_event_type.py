# Assign priority level based on the event type detected after the SIEM scan
# The assigned priority level responds to a scale of 1 to 5, where 1 is the least critical and 5 is the most critical, based on security best practices

from typing import Any, Dict
import logging

# Mapping of event types to priority levels (1-5)
EVENT_PRIORITY_MAP = {
    # High Priority (5)
    'DATA_EXFILTRATION': 5,
    'MALWARE_DETECTED': 5,
    'SQL_INJECTION': 5,
    
    # Medium-High Priority (4)
    'SSH_BRUTE_FORCE': 4,
    'WEB_ATTACK': 4,
    
    # Medium Priority (3)
    'UNAUTHORIZED_ACCESS': 3,
    'RDP_LOGIN_FAILED': 3,
    
    # Low-Medium Priority (2)
    'LOGIN_FAILED': 2,
    'PORT_SCAN': 2,
    
    # Low Priority (1)
    'LOGIN_SUCCESS': 1
}

def assign_priority_by_event_type(event_type: str) -> int:
    priority = EVENT_PRIORITY_MAP.get(event_type, 0)
    
    if priority == 0:
        logging.warning(f"[WARNING]: Unknown event type '{event_type}'. Assigned priority 0.")
    else:
        logging.debug(f"[DEBUG]: Assigned priority {priority} for event type '{event_type}'.")
        
    return priority
