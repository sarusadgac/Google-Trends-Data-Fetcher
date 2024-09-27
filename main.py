# This Python script automatically collects Google Trends data from 51 countries and saves it in JSON and plain text files.
# Additionally, the obtained trend data is added to the README.md file and continuously updated.
# Data sources are taken from Google Trends, and the country pn codes were verified on 26-09-2024.
# If this code is referenced in other projects or publications, proper citation is requested.
# Author: sarusadgac
import feedparser
from datetime import datetime
import os
import json
from countries import country_codes
from flags import country_flags  # Importing flags from flags.py

# Fetch Google Trends data for a specific country
def get_google_trends(country_code):
    url = f"https://trends.google.com/trends/hottrends/atom/feed?pn={country_code}"
    feed = feedparser.parse(url)
    
    trends = []
    for entry in feed.entries:
        trends.append({
            "title": entry.title,
            "link": entry.link,
            "pubdate": entry.published
        })
    
    return trends

# Save data to a JSON file
def save_to_json(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Save data to a plain text file
def save_to_text(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(item['title'] + "\n")

# Get the current timestamp
def get_current_time():
    return datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

# Update the README.md file with the latest trends and timestamps
def update_readme(trend_data):
    current_time = get_current_time()
    
    # Starting content for the README file with the Flag column
    readme_content = f"""
## Google Trends Data Fetcher

Using Google Trends data, this tool automatically collects and updates the most popular search trends from 51 different countries on a regular basis.

Last Update {current_time}

| Country | Flag | Trends | Last Update |
| --- | --- | --- | --- |
"""
    # Adding trends, flags, and last update time for each country
    for country, info in trend_data.items():
        trends_string = ', '.join(info['trends'])  # Join trends with commas
        flag = country_flags.get(country, "")  # Get flag for the country from flags.py
        readme_content += f"| {country} | ![Flag]({flag}) | {trends_string} | {info['last_update']} |\n"

    # Update the README content
    readme_content += f"\n\n## Author\n\nAuthor [sarusadgac](https://x.com/sarusadgac)\n"

    # Write the content to README.md
    with open("README.md", "w", encoding="utf-8") as f:  # UTF-8 encoding for emoji compatibility
        f.write(readme_content)

# Main workflow
def main():
    trend_data = {}  # Dictionary to store trends and update times for each country
    
    # Loop through each country and fetch trends
    for country, code in country_codes.items():
        print(f"Fetching trends for {country}...")
        
        # Fetch Google Trends data
        trends = get_google_trends(code)
        
        # Save the data as JSON and text
        json_filename = f"./json_data/{country}.json"
        text_filename = f"./text_data/{country}.txt"
        save_to_json(json_filename, trends)
        save_to_text(text_filename, trends)
        
        # Store the trends and last update time
        trend_data[country] = {
            "trends": [trend['title'] for trend in trends],
            "last_update": get_current_time()
        }
    
    # Update the README.md file
    update_readme(trend_data)

if __name__ == "__main__":
    main()
