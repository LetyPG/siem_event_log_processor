# Data generator for SIEM event log file processor within the network security domain
# Uses Faker library to generate realistic test data and demo data

from faker import Faker
import random



from src.basic_functions.assign_priority_by_event_type import assign_priority_by_event_type

fake = Faker()


# Event types commonly found in SIEM systems
EVENT_TYPES = [
    'LOGIN_FAILED',
    'LOGIN_SUCCESS',
    'SSH_BRUTE_FORCE',
    'WEB_ATTACK',
    'SQL_INJECTION',
    'RDP_LOGIN_FAILED',
    'PORT_SCAN',
    'MALWARE_DETECTED',
    'UNAUTHORIZED_ACCESS',
    'DATA_EXFILTRATION'
]

# Different datetime formats to test normalization
DATETIME_FORMATS = [
    'with_timezone_offset',  # 2024/09/01 14:23:01-0400
    'with_zulu',             # 2024-09-01T14:25:37Z
    'without_timezone',      # 09-01-2024 15:00:15
    'with_plus_timezone'     # 2024-09-02 09:10:00 +0000
]

# Generate a single realistic SIEM event with random data, asigne a DateTime format, and returns this data as a dictionary
def generate_siem_event(datetime_format: str = None) -> dict:
    if datetime_format is None:
        datetime_format = random.choice(DATETIME_FORMATS)
    
    # Generate random datetime
    dt = fake.date_time_between(start_date='-30d', end_date='now')
    
    # Format datetime based on specified format
    if datetime_format == 'with_timezone_offset':
        formatted_dt = dt.strftime('%Y/%m/%d %H:%M:%S-0400')
    elif datetime_format == 'with_zulu':
        formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif datetime_format == 'without_timezone':
        formatted_dt = dt.strftime('%m-%d-%Y %H:%M:%S')
    elif datetime_format == 'with_plus_timezone':
        formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S +0000')
    else:
        formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    event_type = random.choice(EVENT_TYPES)
    priority = assign_priority_by_event_type(event_type)
    
    return {
        'datetime': formatted_dt,
        'source_ip': fake.ipv4(),
        'destination_ip': fake.ipv4(),
        'port': random.choice([22, 80, 443, 3389, 8080, 3306, 5432]),
        'event_type': event_type,
        'priority': priority
    }

# Generate multiple SIEM events in CSV format,  counting the number of events and including edge cases (invalid data), returns this data as a string
def generate_siem_events_csv(count: int = 10, include_edge_cases: bool = False) -> str:
    events = []
    
    for i in range(count):
        event = generate_siem_event()
        csv_line = f"{event['datetime']},{event['source_ip']},{event['destination_ip']},{event['port']},{event['event_type']},{event['priority']}"
        events.append(csv_line)
  
    if include_edge_cases:
        # Adding some edge cases for testing
        events.append("linea,invalida")  # Invalid line
        events.append("2024/09/01 14:23:01-0400,192.168.1.10,172.16.0.1,443,LOGIN_FAILED,notanumber")  # Invalid priority
    
    return "\n".join(events) + "\n"

# Generate test data specifically designed for unit testing, includes valid events with different datetime formats and edge cases
def generate_test_data_with_edge_cases() -> str:
    events = []
    
    # Event 1: with timezone offset -0400
    event1 = generate_siem_event('with_timezone_offset')
    event1['priority'] = 3  # Medium threat
    csv1 = f"{event1['datetime']},{event1['source_ip']},{event1['destination_ip']},{event1['port']},{event1['event_type']},{event1['priority']}"
    events.append(csv1)
    
    # Event 2: with Zulu timezone
    event2 = generate_siem_event('with_zulu')
    event2['priority'] = 5  # High threat
    csv2 = f"{event2['datetime']},{event2['source_ip']},{event2['destination_ip']},{event2['port']},{event2['event_type']},{event2['priority']}"
    events.append(csv2)
    
    # Event 3: without timezone
    event3 = generate_siem_event('without_timezone')
    event3['priority'] = 1  # Low threat
    csv3 = f"{event3['datetime']},{event3['source_ip']},{event3['destination_ip']},{event3['port']},{event3['event_type']},{event3['priority']}"
    events.append(csv3)
    
    # Edge case 1: Invalid line format
    events.append("linea,invalida")
    
    # Edge case 2: Invalid priority (not a number)
    event_invalid = generate_siem_event('with_timezone_offset')
    csv_invalid = f"{event_invalid['datetime']},{event_invalid['source_ip']},{event_invalid['destination_ip']},{event_invalid['port']},{event_invalid['event_type']},notanumber"
    events.append(csv_invalid)
    
    return "\n".join(events) + "\n"

# Generate demo data with varied datetime formats, returns this data as a string
def generate_demo_data(count: int = 10) -> str:
    return generate_siem_events_csv(count=count, include_edge_cases=False)
