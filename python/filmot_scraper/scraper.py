import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = "https://filmot.com/search/{query}/1?startDuration=0&endDuration={duration}&gridView=1"

def fetch_filmot_data(query: str, duration: int = 300):
    """Fetch and parse Filmot search results."""
    url = BASE_URL.format(query=query, duration=duration)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    soup = BeautifulSoup(response.text, "lxml")

    script_tag = soup.find("script", string=re.compile(r"window\.results\s*=\s*{"))

    if script_tag:
        # Extract the JavaScript content
        script_content = script_tag.string

        # Use regex to extract the JSON portion
        match = re.search(r"window\.results\s*=\s*({.*});", script_content, re.DOTALL)
        
        if match:
            json_str = match.group(1)

            try:
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError as e:
                print("JSON parsing error:", e)
                return None
        else:
            print("window.results not found in script tag")
            return None
    else:
        print("Script tag containing window.results not found")
        return None