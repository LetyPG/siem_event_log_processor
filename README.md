# SIEM Event Log File Processor

This project involves creating a Python program to automate actions for checking log information on a security monitoring program within a network. The program processes security events archived in a specific log file as input, following a defined format.
The program is built using the Functional Programming Paradigm intented to:

- After previous problem analysis, was determined that the system will consume the and process the event log data separated as string, numbers and dates, so it will not be focused on the event log file as an object instance, but as a list of dictionaries.
- Each function designed as a basic function is responsible for a specific task, making the code more modular and easier to maintain and keeping the cohesion principle.
- Only one function is the principle module called as complex function, it is going to call the other functions to process the event log file, is recomended used the mininmal number of parameters (functions) to pass to the complex function, to control the acoplament risk of the system.

## QA Perspective

As a QA professional behind of the project, I include this practice:

- A demo to validate the functionality of the program
- A test directory to validate the functionality of each function and the complex function.
- A helper directory to manage test environment, data and logging to avoid code duplication and hardcode.

## Project Documentation

The project documentation is as follows:

- [Project Documentation](docs/project_doc.md)

## Quick UI View

<p align="center">
<img src="ui/static/images/siem_event_log_file_processor.png" alt="SIEM Event Log File Processor">
</p>

## Directory Structure

The directory structure is as follows:

```
|__siem_event_log_file_processor/                       # Main directory for the project.
|   |__src/                                             # Main source code file for the project, contains pure functions and complex function.
|   |   |__basic_functions/
|   |   |   |__read_events_from_file.py
|   |   |   |__normalize_event_datetime.py
|   |   |   |__add_threat_level_by_priority.py
|   |   |   |__assign_priority_by_event_type.py
|   |   |__complex_processor_functions/
|   |   |   |__combined_processor_functions.py
|   |__ui/                                              # Web-based UI for event visualization (MVC architecture)
|   |   |__app.py                                       # Main Flask application
|   |   |__models/
|   |   |   |__event_model.py                           # Data handling and business logic
|   |   |__routes/
|   |   |   |__event_routes.py                          # Route controllers and API endpoints
|   |   |__views/
|   |   |   |__templates/
|   |   |   |   |__dashboard.html                       # Main dashboard template
|   |   |__static/
|   |   |   |__css/
|   |   |   |   |__style.css                            # Dashboard styling
|   |   |   |__js/
|   |   |   |   |__dashboard.js                         # Client-side interactivity
|   |__demo/                                            # Demo file for the project, validate the functionality of the program.
|   |   |__demo_event_siem_log_processor.py
|   |__tests/                                           # Test file for the project, contains unit tests to validate requirements for each function.
|   |   |__test_read_events_from_file.py
|   |   |__test_normalize_event_datetime.py
|   |   |__test_add_threat_level_by_priority.py
|   |   |__test_assign_priority_by_event_type.py
|   |   |__test_combine_read_file_normalize_timestamp_add_threat_level.py
|   |   |__test_data_generator.py
|   |__helpers/                                         # Helper file for the project, contains helper classes to manage test environment, data and logging.
|   |   |__test.py                                      # Test base class
|   |   |__data_generator.py                            # Faker-based data generator
|   |__README.md                                        
|   |__diagram.md
|   |__requeriments.txt
|

### Tech Stack used:
- Python           3.13.4 
- python-dateutil  2.9.0
- pytz             2025.2
- Faker            >=28.0.0
- Flask            >=3.0.0 (for web UI)
- pytest           (for testing)
- unittest         (built-in)

```

## Using the project

To use the project you can fallow the next steps:

1. Clone the repository (or download the zip file):

```bash
git clone https://github.com/letyPG/siem_event_log_file_processor.git
```

2. Create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install the requirements:

```bash
pip install -r requeriments.txt
```

5. Run the demo:

```bash
python3 -m demo.demo_event_siem_log_processor
```

6. Run the tests (More info in the tests directory):

```bash
python3 -m pytest tests/ -v
```

7. Run the Web UI (Optional):

- By default the web ui will run on port 5000:

```bash
cd ui
python3 app.py
```

- If you want to run the web ui on a different port, you can use the PORT environment variable:

```bash
cd ui
PORT=8000 python3 app.py
```

Then open your browser to `http://localhost:5000` to access the dashboard, or `http://localhost:8000` if you used a different port.

>For this project was used python3, if you are want to use a different version, please use the current version of python and you can be able to run the commands without any issue, for example instead of `python3` you can use `python`.

8. Generate a new event log file (Optional):

- Open new terminal and run the next command:
`python3 -m venv venv`

- Activate the virtual environment:
`source venv/bin/activate`

- Install the requirements:
`pip install -r requeriments.txt`

- Run the demo:
`python3 -m demo.demo_event_siem_log_processor`

```bash
pyton3 -m demo.demo_event_siem_log_processor
```

- The demo will generate a new event log file and process it
- Go to the browser and refresh the page to see the new events
- If you want to verify if the events are processed correctly, you can check the `processed_events.json` file in the root directory and select the event IP that you want to see in the web ui, go to the `Events` tab and introduce the IP in the filter input.

9. Stop the Web UI (Optional):

```bash
Ctrl+C
```

## Source Code (`src/`)

### Pure Functions (`src/basic_functions/`)

- `read_events_from_file.py` (Reads events from a CSV file)
- `normalize_event_datetime.py` (Normalizes event datetime)
- `assign_priority_by_event_type.py` (Assigns priority by event type)
- `add_threat_level_by_priority.py` (Adds threat level by priority)

### Complex Function (`src/complex_function/`)

- `combined_processor_functions.py` (Combines all the pure functions to process the event log file)

## Web UI (`ui/`)

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

### Files

- `app.py` (Main Flask application)
- `models/event_model.py` (Data handling and business logic)
- `routes/event_routes.py` (Route controllers and API endpoints)
- `views/templates/dashboard.html` (Main dashboard template)
- `views/static/css/style.css` (Dashboard styling)
- `views/static/js/dashboard.js` (Client-side interactivity)

## Copyright & License

© 2025 LetyPG. All Rights Reserved.

This project is part of a professional portfolio and is intended for demonstration and educational purposes. Unauthorized copying, modification, distribution, or use of this code for commercial purposes is strictly prohibited without explicit permission from the author.
