import os
import json
from datetime import datetime

# Function to get current timestamp
def get_current_time():
    return datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

# Function to generate the HTML page
def generate_html():
    countries_data = {}

    # Read data from each country's JSON file
    json_dir = './json_data'
    for json_file in os.listdir(json_dir):
        country_name = json_file.replace('.json', '')
        with open(os.path.join(json_dir, json_file), 'r', encoding='utf-8') as f:
            country_trends = json.load(f)
            trends_list = [trend['title'] for trend in country_trends]
            countries_data[country_name] = {
                'trends': ', '.join(trends_list),
                'last_update': get_current_time()
            }

    # Start generating HTML content with Simple.css included
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Trends Data Fetcher</title>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
    </head>
    <body>
        <header>
            <h1>Google Trends Data Fetcher</h1>
            <p>Using Google Trends data, this tool automatically collects and updates the most popular search trends from 51 different countries on a regular basis.</p>
        </header>
        <main>
            <table>
                <thead>
                    <tr>
                        <th>Country</th>
                        <th>Flag</th>
                        <th>Trends</th>
                        <th>Last Update</th>
                    </tr>
                </thead>
                <tbody>
    """

    # Sort countries, with Turkey at the top
    sorted_countries = sorted(countries_data.items())
    sorted_countries = [('TURKIYE', countries_data.pop('TURKIYE'))] + sorted_countries

    # Add each country's data to the HTML table
    for country, info in sorted_countries:
        flag_url = f"https://flagcdn.com/16x12/{country.lower()[:2]}.png"
        html_content += f"""
                    <tr>
                        <td>{country}</td>
                        <td><img src="{flag_url}" alt="{country} Flag"></td>
                        <td>{info['trends']}</td>
                        <td>{info['last_update']}</td>
                    </tr>
        """

    # Close table and HTML tags
    html_content += """
                </tbody>
            </table>
        </main>
        <footer>
            <p>Author: <a href="https://x.com/sarusadgac">sarusadgac</a></p>
        </footer>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

# Main function
if __name__ == "__main__":
    generate_html()
