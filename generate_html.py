import os
import json
from datetime import datetime

# Folder containing the JSON files
json_folder = "./json_data"

# Function to generate HTML
def generate_html():
    # Initial HTML structure and Simple.css integration
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Trends Data</title>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.css">
    </head>
    <body>
        <header>
            <h1>Google Trends Data Fetcher</h1>
            <p>This page displays the most popular search trends from various countries, updated regularly.</p>
        </header>
        <section>
    """
    
    # Read JSON files and convert them into tables
    for country_file in os.listdir(json_folder):
        if country_file.endswith(".json"):
            country_name = country_file.replace(".json", "")
            
            with open(os.path.join(json_folder, country_file), "r", encoding="utf-8") as f:
                trends = json.load(f)
            
            # Create a table for each country
            html_content += f"""
            <h2>Trend Data for {country_name}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Link</th>
                        <th>Publish Date</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            # Add each trend as a row in the table
            for trend in trends:
                html_content += f"""
                <tr>
                    <td>{trend['title']}</td>
                    <td><a href="{trend['link']}">{trend['title']}</a></td>
                    <td>{trend['pubdate']}</td>
                </tr>
                """
            
            html_content += "</tbody></table>"
    
    # Closing the HTML structure with a footer
    html_content += """
        </section>
        <footer>
            <p>Author <a href="https://x.com/sarusadgac">sarusadgac</a></p>
            <p>Last Update: {}</p>
        </footer>
    </body>
    </html>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Save the generated HTML file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML file generated successfully!")

# Main function
if __name__ == "__main__":
    generate_html()
