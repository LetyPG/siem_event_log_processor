# Execute the demo script to process security events from a file and output the results in JSON format.
# This script is used to verify the functionality of the SIEM event log file processor using the combined_processor_functions module.


import os
import json
from src.complex_processor_functions.combined_processor_functions import combine_read_file_normalize_timestamp_add_threat_level
from helpers.data_generator import generate_demo_data
import logging

if __name__ == "__main__": 
    
    # Json file to store the processed events
    output_file = "processed_events.json"

    # Generate realistic sample data using Faker
    print("Generating realistic SIEM event data...")
    sample_data = generate_demo_data(count=15)
    
    file_name = "events_siem.txt"
    with open(file_name, "w") as f:
        f.write(sample_data)

    logging.info(f"Procesando eventos desde '{file_name}'...")
    # Check if the file exists and proceed to process the events
    final_events = combine_read_file_normalize_timestamp_add_threat_level(file_name)

    # Print the processed events to the console in JSON format
    logging.info("Processed events:")
    output_file = "processed_events.json"
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(final_events, out, indent=2)
        print(f"Results archived in '{output_file}'.")

    # Print the number of processed events
    if final_events:
        logging.info(f"[INFO] It was processed {len(final_events)} events.")

    # Clean up the created file after processing
    if os.path.exists(file_name):
        os.remove(file_name)

    logging.info("[INFO] Demo completed successfully.")
    
    # bash : python -m demo.demo_event_siem_log_processor
   
