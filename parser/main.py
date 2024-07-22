import requests
from bs4 import BeautifulSoup
import json

# URL of the AJAX endpoint
url = "https://schema.mau.se/ajax/ajax_resurser.jsp?op=hamtaAllaKurser"

# Fetch the page content
response = requests.get(url)
response.raise_for_status()  # Ensure we got a successful response

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all <a> tags within the <ul> tags
course_links = []
uls = soup.find_all('ul')
for ul in uls:
    links = ul.find_all('a', href=True)
    for link in links:
        course_links.append(link['href'])

# Create a dictionary for the JSON output
output = {'links': course_links}

# Save the JSON output to a file
with open('course_links.json', 'w') as json_file:
    json.dump(output, json_file, indent=4)

print("Course links have been saved to course_links.json")
