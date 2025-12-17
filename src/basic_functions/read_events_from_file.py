# Read events from file and return a list of dictionaries

import csv 
from typing import Any, Dict, List 
import logging 



KEYS = ['datetime', 'source_ip', 'destination_ip', 'port', 'event_type', 'priority']

                                      
def read_events_from_file(file_path: str) -> List[Dict[str, Any]]:  
    events = []                        
    try:                            
        with open(file_path, mode='r', encoding='utf-8') as f: 
            reader = csv.reader(f)    
            for row in reader:        
                if len(row) == len(KEYS):
                    event_dict = dict(zip(KEYS, row))
                    try:               
                        event_dict['port'] = int(event_dict['port']) 
                        event_dict['priority'] = int(event_dict['priority'])
                        events.append(event_dict)
                    except ValueError:
                        logging.warning(f"[WARNING]: It was omitted a line due to invalid data (port/priority): {row}")
                elif not all(row):    
                    logging.warning(f"[WARNING]: It was omitted a line due to empty fields: {row}") 
    except FileNotFoundError:
        logging.error(f"[ERROR]: The file in the path '{file_path}' was not found.") 
    return events   