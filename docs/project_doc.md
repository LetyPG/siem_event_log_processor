
# Main Source Code (`src/basic_functions/`)

**Packages and Modules Imported:**

- `csv`: Reads and writes CSV files, useful for processing event logs separated by commas.
- `typing` (`Any`, `Dict`, `List`): Defines variable and function types.
- `logging`: Prints log messages for debugging and tracking program flow.
- `dateutil.parser`: Handles multiple date formats (external dependency).
- `pytz`: Manages different time zones (external dependency).

## Functions

### Read Events from File (`src/basic_functions/read_events_from_file.py`)

**Functionality**  
Reads a file and returns a list of dictionaries, each representing a security event with keys: `datetime`, `source_ip`, `destination_ip`, `port`, `event_type`, and `priority`.

<details><summary>Enviroment Variables</summary>

**KEYS:** Event data constants as a format information on the logs events file

</details>

<details><summary>Resolution Steps:</summary>

1. **Define Function Signature:**

    ```python
    def read_events_from_file(file_path: str) -> List[Dict[str, Any]]:
    ```

2. **Initialize Events List:**  
    Create an empty list to store events.
3. **Open File and Handle Exceptions:**  
    Use `try`/`except` and `with open(file_path, 'r', encoding='utf-8') as f`.
4. **Read File Line by Line:**  
    Use `csv.reader` to iterate over rows.
5. **Validate Row and Create Event Dictionary:**  
    Use `zip` to combine keys and values.
6. **Validate and Add Event:**  
    Convert `port` and `priority` to integers, handle conversion errors.
7. **Handle Empty Rows:**  
    Log warnings for empty rows.
8. **Handle Exceptions:**  
    Log errors for file issues.
9. **Return Events List:**  
    Return the list of event dictionaries.

</details>

### Normalize Event Datetime (`src/basic_functions/normalize_event_datetime.py`)

**Functionality**  
Normalizes a datetime string to a specific format (YYYY-MM-DD HH:MM:SS) and handles timezone conversion to UTC.

<details><summary>Resolution Steps:</summary>

2. **Get Raw Datetime Value:**  
    Use `event.get('datetime')`.
3. **Check for Empty/None Datetime:**  
    Return event as is if empty.
4. **Parse Datetime:**  
    Use `dateutil.parser.parse`.
5. **Set Timezone to UTC if Missing:**  
    Use `replace(tzinfo=pytz.UTC)`.
6. **Convert to UTC and Format:**  
    Use `astimezone(pytz.UTC)` and `strftime('%Y-%m-%d %H:%M:%S')`.
7. **Handle Exceptions:**  
    Set `datetime` to `"Formato Desconocido"` on error.
8. **Return Modified Event:**  
    Return event with normalized datetime.

</details>

### Assign Priority by Event Type (`src/basic_functions/assign_priority_by_event_type.py`)

**Functionality**  
Assigns a priority level based on the type of a security event, and the best practices, common for SIEM systems. It was considered a range of 1 to 5, where 1 is the least critical and 5 is the most critical.

<details><summary>Enviroment Variables</summary>

**EVENT_PRIORITY_MAP:**

- High Priority (5)
    'DATA_EXFILTRATION': 5,
    'MALWARE_DETECTED': 5,
    'SQL_INJECTION': 5,

- Medium-High Priority (4)
    'SSH_BRUTE_FORCE': 4,
    'WEB_ATTACK': 4,

- Medium Priority (3)
    'UNAUTHORIZED_ACCESS': 3,
    'RDP_LOGIN_FAILED': 3,

- Low-Medium Priority (2)
    'LOGIN_FAILED': 2,
    'PORT_SCAN': 2,

- Low Priority (1)
    'LOGIN_SUCCESS': 1

</details>

<details><summary>Resolution Steps:</summary>

1. Define Function Signature:

```python
    def assign_priority_by_event_type(event: Dict[str, Any]) -> Dict[str, Any]:
```

2. **Get Event Type Value:**
    Use `event.get('event_type')` to consume the event type from the event dictionary.
3. **Check Event Type :**
    Use `isinstance(event_type, str)`.
4. **Get Priority Value:**
    Use `EVENT_PRIORITY_MAP.get(event_type, 0)`.
5. **Check Priority Value:**
    Use `if priority == 0`.
6. **Add Priority to Event:**
    Set `event['priority']`.
7. **Return Modified Event:**
    Return event with priority.

</details>  

### Add Threat Level by Priority (`src/basic_functions/add_threat_level_by_priority.py`)

**Functionality**  
Assigns a threat level based on the priority of a security event.

<details><summary>Enviroment Variables</summary>

**Threat Level Mapping:**

- Low: priority 1-2
- Medium: priority 3-4
- High: priority 5
- Unknown: any other priority

</details>

<details><summary>Resolution Steps:</summary>

1. Define Function Signature:

```python
    def add_threat_level_by_priority(event: Dict[str, Any]) -> Dict[str, Any]:
```

2. **Get Priority Value:**
    Use `event.get('event_type')`.
3. **Consume Priority Value:**
    Use `assign_priority_by_event_type(event_type)`.
4. **Initialize Threat Level:**
    Default to `"Unknown"`.
5. **Check Priority Type:**
    Use `isinstance(priority, int)`.
6. **Map Priority to Threat Level:**
    Use `THREAT_LEVEL_MAP` dictionary.
6. **Add Threat Level to Event:**
    Set `event['threat_level']`.
7. **Return Modified Event:**
    Return event with threat level.

</details>

----

### Combined Processor File Functions (`src/complex_processor_functions/combined_processor_functions.py`)

**Functionality:**  
Combines previous functions to read, normalize, and enrich events.

<details><summary>Resolution Steps:</summary>

1. **Define Function Signature:**

    ```python
    def combine_read_file_normalize_timestamp_add_threat_level(file_path: str, max_events: int = 100000) -> List[Dict[str, Any]]:
    ```

2. **Read Events from File:**  
    Call `read_events_from_file`.
3. **Validate Events:**  
    Return empty list if no valid events.
4. **Check Event Limit:**  
    Raise `ValueError` if exceeding `max_events`.
5. **Log Event Count and File Path.**
6. **Process Each Event:**  
    Use list comprehension to apply `normalize_event_datetime` and `add_threat_level`.
7. **Return Processed Events:**  
    Return list of processed event dictionaries.

>Note: The limit events was considered to avoid overloading of the system on its processing

</details>

**Command to run the function:**

```bash
python3 -m src.complex_processor_functions.combined_processor_functions
```

----

## Demo program (`demo/`)

The demo program is a simple script that demonstrates the use of the functions in the project.

**Command to run the module:**
    ```bash
    python3 -m demo.demo_event_siem_log_processor
    ```

----

## Unit Tests (`tests/`)

`test_read_events_from_file.py`
`test_normalize_event_datetime.py`
`test_add_threat_level_by_priority.py`
`test_combine_read_file_normalize_timestamp_add_threat_level.py`

**Test Criteria:**

- Expected output matches actual output (using `assert`).
- Input validation and error handling.
- Robustness against corrupted data.

**Test Runner:**

- Uses `unittest.main()` to execute tests when run directly.

**Test Data:**

- The test logic is isolated from the main application logic, and only focus on it, for that reason and also to avoid any side effects such as hardcoded data, the test data is generated using the `helpers/data_generator.py` module.
- Consumes test data from `helpers/data_generator.py.generate_siem_event_csv` and `helpers/data_generator.py.generate_test_data_with_edge_cases`

**Command to run the module:**
    ```bash
    python3 -m pytest tests/
    ```

----

## Web UI Dashboard (`ui/`)

A modern web-based dashboard for visualizing and monitoring SIEM events in real-time.

### Features

**Statistics Dashboard**

- Total events count
- Threat level distribution (High, Medium, Low)
- Last updated timestamp
- Real-time refresh capability

**Advanced Filtering**

- Filter by threat level
- Search by source IP address
- Adjustable result limits (50/100/200/500)
- Clear filters option

**Event Table**

- Color-coded threat levels (🔴 High, 🟡 Medium, 🟢 Low)
- Sortable columns
- Responsive design
- Smooth animations

**Modern Design**

- Professional dark theme
- Card-based layout
- Gradient headers
- Micro-animations

### Running the UI

### API Endpoints

The UI provides RESTful API endpoints for programmatic access:

**GET `/api/events`** - Get all events or filtered events

- Query params: `threat_level`, `source_ip`, `limit`

**GET `/api/events/stats`** - Get event statistics

- Returns total counts and threat distribution

**GET `/api/events/recent`** - Get recent events

- Query param: `limit` (default: 10)

### Architecture

The UI follows MVC (Model-View-Controller) pattern:

- **Model** (`models/event_model.py`) - Data handling and business logic
- **View** (`views/templates/dashboard.html`) - HTML template and presentation
- **Controller** (`routes/event_routes.py`) - Route handlers and API logic

### Integration

The UI integrates seamlessly with the existing SIEM processor:

- Reads from `processed_events.json` generated by the demo or processing functions
- Uses the same data structures and threat level mappings
- Can be extended to trigger event processing via API
