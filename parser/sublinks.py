import os
import requests
from bs4 import BeautifulSoup
import json

# Function to fetch data from each course link
def fetch_course_data(course_url):
    response = requests.get(course_url)
    response.raise_for_status()  # Ensure we got a successful response
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try to find the <ul class="resursLista">
    resurs_lista = soup.find('ul', class_='resursLista')
    
    if resurs_lista:
        # Extract all links within the <ul class="resursLista">
        links = resurs_lista.find_all('a', href=True)
        return [link['href'] for link in links]
    else:
        # If <ul class="resursLista"> is not found, find the <tbody>
        tbody = soup.find('tbody')
        if tbody:
            # Extract the last part of the URL for naming the file
            file_name_part = course_url.split('=')[-1]
            file_name = f"{file_name_part}_table.html"
            with open(file_name, 'w') as file:
                file.write(str(tbody))
            return None
        return None

# Load the course links from course_links.json
with open('course_links.json', 'r') as file:
    data = json.load(file)
    course_links = data['links']

# Dictionary to store the results
results = {}

# Visit each course link and fetch data
for link in course_links:
    full_url = f"https://schema.mau.se/{link}"
    print(f"Fetching data from {full_url}")
    course_data = fetch_course_data(full_url)
    if course_data:
        results[link] = course_data

# Save the results to a new JSON file
with open('course_data.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

print("Course data has been saved to course_data.json")
