# Normalize the timestamp to UTC,format it and return a list of dictionaries with the normalized timestamp

from typing import Any, Dict
import logging 
from dateutil import parser 
import pytz



def normalize_event_datetime(event: Dict[str, Any]) -> Dict[str, Any]: 
    raw_datetime = event.get('datetime')        
    if not raw_datetime:                         
        return event
    try:                                         
        parsed_dt = parser.parse(raw_datetime)   
        if parsed_dt.tzinfo is None:            
            parsed_dt = parsed_dt.replace(tzinfo=pytz.utc)
        utc_dt = parsed_dt.astimezone(pytz.utc)   
        event['datetime'] = utc_dt.strftime('%Y-%m-%d %H:%M:%S') 
    except (parser.ParserError, TypeError) as e:
        logging.warning(f"[WARNING]: It was not possible to process the date '{raw_datetime}'. Error: {e}") 
        event['datetime'] = "Unknown Format"
    return event                               
