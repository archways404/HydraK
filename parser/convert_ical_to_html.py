import os
import json
from icalendar import Calendar, Event
import re

def parse_summary(summary):
    fields = {
        "Kurs.grp": None,
        "Sign": None,
        "Moment": None,
        "Aktivitetstyp": None
    }

    kurs_grp_match = re.search(r'Kurs\.grp:\s*([^,]+)', summary)
    sign_match = re.search(r'Sign:\s*([^,]+)', summary)
    moment_match = re.search(r'Moment:\s*([^,]+)', summary)
    aktivitetstyp_match = re.search(r'Aktivitetstyp:\s*([^,]+)', summary)

    if kurs_grp_match:
        fields["Kurs.grp"] = kurs_grp_match.group(1)
    if sign_match:
        fields["Sign"] = sign_match.group(1)
    if moment_match:
        fields["Moment"] = moment_match.group(1)
    if aktivitetstyp_match:
        fields["Aktivitetstyp"] = aktivitetstyp_match.group(1)

    return fields

def ical_to_json(ical_file_path):
    try:
        with open(ical_file_path, 'r') as f:
            ical_content = f.read()

        calendar = Calendar.from_ical(ical_content)
        events = []

        for component in calendar.walk():
            if component.name == "VEVENT":
                event = {}
                for key, value in component.items():
                    event[key] = str(value)

                # Parse and include additional fields from SUMMARY
                if "SUMMARY" in event:
                    additional_fields = parse_summary(event["SUMMARY"])
                    event.update(additional_fields)
                
                events.append(event)
        
        return events

    except Exception as e:
        print(f"Error processing file {ical_file_path}: {e}")
        return []

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def convert_all_icals_to_json(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    json_output_folder = 'C:/Users/archways/Documents/GitHub/HydraK/parser/JSON'
    ensure_directory_exists(json_output_folder)

    ical_files = [f for f in os.listdir(folder_path) if f.endswith('.ical')]
    
    if not ical_files:
        print("No .ics files found in the specified folder.")
        return

    for ical_file in ical_files:
        ical_file_path = os.path.join(folder_path, ical_file)
        events = ical_to_json(ical_file_path)
        
        if events:
            json_file_name = os.path.splitext(ical_file)[0] + '.json'
            json_file_path = os.path.join(json_output_folder, json_file_name)
            with open(json_file_path, 'w') as json_file:
                json.dump(events, json_file, indent=2)
            print(f"Converted {ical_file} to {json_file_name}")
        else:
            print(f"No events found in {ical_file}")

# Specify your folder containing the iCal files
folder_path = 'C:/Users/archways/Documents/GitHub/HydraK/parser/ical-files'
convert_all_icals_to_json(folder_path)
