
<!--this is a comment -->

# SIEM Event Log File Processor Flowchart

```mermaid
graph TD;
    siem_scanner-->events_log_file;
    events_log_file-->read_events;
    events_log_file-->normalize_timestamp;
    events_log_file-->assign_priority;
    assign_priority-->add_threat_level;
    read_events-->combine_read_files_normalize_timestamp_add_threat_level;
    normalize_timestamp-->combine_read_files_normalize_timestamp_add_threat_level;
    add_threat_level-->combine_read_files_normalize_timestamp_add_threat_level;
    combine_read_files_normalize_timestamp_add_threat_level-->read;
    read-->timestamp;
    timestamp-->threat_level;
    threat_level-->final_processed_events;
    
```

## SIEM Event Log File Processor State Diagram

```mermaid
stateDiagram-v2
    [*] --> Network_activity
    Network_activity --> siem_scanner
    siem_scanner --> events_log_file
    events_log_file --> read_events
    events_log_file --> normalize_timestamp
    events_log_file --> assign_priority
    assign_priority --> add_threat_level
    read_events --> combine_read_files_normalize_timestamp_add_threat_level
    normalize_timestamp --> combine_read_files_normalize_timestamp_add_threat_level
    add_threat_level --> combine_read_files_normalize_timestamp_add_threat_level
    combine_read_files_normalize_timestamp_add_threat_level --> read
    read --> timestamp
    timestamp --> threat_level
    threat_level --> final_processed_events
    final_processed_events --> dashboard_UI
    dashboard_UI --> [*]
    
```

## Pure Functions Diagram

### Read Events from File

**File:** `src/basic_functions/read_events_from_file.py`
**Test:** `tests/test_read_events_from_file.py`

```mermaid
graph TD
    Start([Start]) --> Init[Initialize empty list]
    Init --> Open{Open File?}
    Open -- Yes --> Read[Read CSV Row]
    Open -- No --> LogError[Log FileNotFoundError] --> End([Return List])
    Read --> Check{Valid Row?}
    Check -- Yes --> Parse[Convert port/priority to int]
    Check -- No --> LogWarn[Log Warning] --> Read
    Parse -- Success --> Add[Append to List] --> Read
    Parse -- Error --> LogWarn2[Log ValueError] --> Read
    Read -- EOF --> End
```

### Normalize Event Datetime

**File:** `src/basic_functions/normalize_event_datetime.py`
**Test:** `tests/test_normalize_event_datetime.py`

```mermaid
graph TD
    Start([Start]) --> Check{Has datetime?}
    Check -- No --> Return([Return Event])
    Check -- Yes --> Parse[Parse datetime string]
    Parse --> TZ{Has Timezone?}
    TZ -- No --> SetUTC[Set to UTC] --> Convert
    TZ -- Yes --> Convert[Convert to UTC]
    Convert --> Format[Format YYYY-MM-DD HH:MM:SS]
    Format --> Update[Update Event] --> Return
    Parse -- Error --> LogWarn[Log Warning]
    LogWarn --> SetUnknown[Set 'Unknown Format'] --> Return
```

### Assign Priority by Event Type

**File:** `src/basic_functions/assign_priority_by_event_type.py`
**Test:** `tests/test_assign_priority_by_event_type.py`

```mermaid
graph TD
    Start([Start]) --> Lookup[Lookup Event Type in Map]
    Lookup --> Found{Found?}
    Found -- Yes --> Return([Return Priority])
    Found -- No --> LogWarn[Log Warning]
    LogWarn --> ReturnZero([Return 0])
```

### Add Threat Level by Priority

**File:** `src/basic_functions/add_threat_level_by_priority.py`
**Test:** `tests/test_add_threat_level_by_priority.py`

```mermaid
graph TD
    Start([Start]) --> CheckType{Has Event Type?}
    CheckType -- Yes --> Call[Call assign_priority_by_event_type]
    Call --> Update{New Priority > 0?}
    Update -- Yes --> SetPriority[Update Event Priority]
    Update -- No --> GetPriority
    CheckType -- No --> GetPriority[Get Priority from Event]
    SetPriority --> GetPriority
    GetPriority --> CheckInt{Is Int?}
    CheckInt -- Yes --> Map[Map Priority to Threat Level]
    CheckInt -- No --> SetUnknown
    Map --> SetLevel[Set Threat Level] --> Return([Return Event])
    SetUnknown[Set 'Unknown'] --> Return
```

### Combine Read File Normalize Timestamp Add Threat Level

**File:** `src/complex_processor_functions/combined_processor_functions.py`
**Test:** `tests/test_combine_read_file_normalize_timestamp_add_threat_level.py`

```mermaid
graph TD
    Start([Start]) --> Read[Read Events from File]
    Read --> Normalize[Normalize Timestamp]
    Normalize --> Add[Add Threat Level]
    Add --> Return([Return Events])
```

## Test Diagram

### Test Functions Diagram

```mermaid
graph TD
    data_generator --> TestEventSiemLogProcessor;
    TestEventSiemLogProcessor--> read_events_from_file --> test_read_events_from_file;
    TestEventSiemLogProcessor--> normalize_event_datetime --> test_normalize_event_datetime;
    TestEventSiemLogProcessor--> assign_priority_by_event_type --> test_assign_priority_by_event_type;
    TestEventSiemLogProcessor--> add_threat_level_by_priority --> test_add_threat_level_by_priority;
    TestEventSiemLogProcessor--> combine_read_file_normalize_timestamp_add_threat_level --> test_combine_read_file_normalize_timestamp_add_threat_level;
   
```

### Test Data Generator Diagram

```mermaid
graph TD 
    data_generator --> test_data_generator;
```
