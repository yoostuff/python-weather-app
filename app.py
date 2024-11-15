from flask import Flask, render_template_string
import json
import plotly.graph_objects as go
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    encoding = 'utf-8'  # Default to 'utf-8'
    if raw_data.startswith(b'\xff\xfe'):
        encoding = 'utf-16'  # Little endian
    elif raw_data.startswith(b'\xfe\xff'):
        encoding = 'utf-16'  # Big endian
    return encoding

# Function to extract JSON data from HTML file
def extract_json_from_html(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as file:
        text = file.read()
        pattern = re.compile(r'\{.*\}', re.DOTALL)  # Regex pattern to match JSON structure
        match = pattern.search(text)
        if match:
            json_text = match.group(0)
            json_data = json.loads(json_text)
            return json_data
        else:
            raise ValueError("Could not find JSON data in the HTML file")

# Function to check for missing alt attributes in images and title attributes in anchors
def check_missing_attributes(content):
    soup = BeautifulSoup(content, 'html.parser')
    missing_alt = [img for img in soup.find_all('img') if not img.get('alt')]
    missing_title = [a for a in soup.find_all('a') if not a.get('title')]
    return len(missing_alt), len(missing_title)

# Function to extract data from JSON
def extract_data_from_json(json_data):
    total_word_count = 0
    total_page_title_length = 0
    total_meta_description_length = 0
    total_keywords_on_page = 0
    total_warnings = 0
    missing_title = 0
    missing_description = 0
    missing_image_alt_text = 0
    missing_anchor_title = 0
    website_name = ""

    for page in json_data['pages']:
        total_word_count += page['word_count']
        total_page_title_length += len(page['title'])
        total_meta_description_length += len(page['description'])
        total_keywords_on_page += len(page['keywords'])

        # Extract website name from the URL if not already set
        if not website_name:
            parsed_url = urlparse(page['url'])
            website_name = parsed_url.netloc

        # Warning conditions
        if page['word_count'] < 300:  # Example condition for low word count
            total_warnings += 1
        if len(page['title']) == 0:
            missing_title += 1
            total_warnings += 1
        if len(page['description']) == 0:
            missing_description += 1
            total_warnings += 1
        
        # Check for missing attributes
        alt_missing, title_missing = check_missing_attributes(page.get('content', ''))
        missing_image_alt_text += alt_missing
        missing_anchor_title += title_missing
        total_warnings += alt_missing + title_missing

        # Count warnings from warnings field
        if 'warnings' in page:
            total_warnings += len(page['warnings'])

    return website_name, [total_word_count, total_page_title_length, total_meta_description_length, total_keywords_on_page, total_warnings, missing_title, missing_description, missing_image_alt_text, missing_anchor_title]

@app.route('/')
def home():
    # Sample data extraction
    file_path = r'C:\Users\HP\Documents\python\seo_results.html'
    try:
        json_data = extract_json_from_html(file_path)
        website_name, values = extract_data_from_json(json_data)
        categories = ['Word Count', 'Page Title', 'Meta Description', 'Keywords On-Page', 'Warnings', 'Missing Title', 'Missing Description', 'Missing Image Alt-Text', 'Missing Anchor Title']

        # Filter out zero values
        filtered_values = [value for value in values if value != 0]
        filtered_categories = [categories[i] for i in range(len(values)) if values[i] != 0]

        # Create a bar chart
        fig = go.Figure(data=[go.Bar(x=filtered_categories, y=filtered_values, marker_color='skyblue')])
        fig.update_layout(title='SEO Analysis Results', xaxis_title=f'SEO Metrics for {website_name}', yaxis_title='Total Count', xaxis_tickangle=-45)

        # Get HTML representation of the plotly figure
        plot_html = fig.to_html(full_html=False)

        # Render the plotly figure in the Flask template
        return render_template_string("""
            <html>
                <head><title>SEO Analysis Results</title></head>
                <body>
                    <h1>SEO Analysis Results</h1>
                    {{ plot_html|safe }}
                </body>
            </html>
        """, plot_html=plot_html)
    except ValueError as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)