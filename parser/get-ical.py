import json
import time
import requests
import os
import re

# Load the course data from course_data.json
with open('course_data.json', 'r') as file:
    course_data = json.load(file)

# Function to fetch and save the .ics file
def fetch_and_save_ical(url, file_name):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"Saved {file_name}")

# Ensure the directory exists
os.makedirs('./ical-files', exist_ok=True)

# Process the course data
urls_to_process = []
for original_url, links in course_data.items():
    for link in links:
        if link != "#":
            # Modify the URL to the required format
            modified_url = link.replace("/Schema.jsp", "/SchemaICAL.ics")
            urls_to_process.append(modified_url)

# Perform requests in batches of 10
batch_size = 10
for i in range(0, len(urls_to_process), batch_size):
    batch = urls_to_process[i:i + batch_size]
    for url in batch:
        # Extract the file name part from the URL
        file_name_part = url.split('resurser=')[-1]
        
        # Clean up the file name to remove invalid characters
        file_name_part = re.sub(r'[^\w\-_\.]', '_', file_name_part)
        file_name = f"./ical-files/{file_name_part}.ical"
        
        # Fetch and save the .ics file
        try:
            fetch_and_save_ical(url, file_name)
        except Exception as e:
            print(f"Failed to save {file_name}: {e}")
    
    # Wait for a minute after processing each batch
    if i + batch_size < len(urls_to_process):
        print("Waiting for a minute before processing the next batch...")
        time.sleep(1)

print("All URLs have been processed.")
