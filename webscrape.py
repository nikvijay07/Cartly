from flask import Flask, request
from flask import jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import os

app = Flask(__name__)

def extract_text_recursive(element):
    """Recursively extract text from nested elements. """
    text = element.text.strip()
    if not text:
        # If the current element has no text, continue recursively with its children
        children = element.find_elements_by_xpath('./*')
        for child in children:
            text += ' ' + extract_text_recursive(child)
    return text

def run_selenium():
    #chrome driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'https://www.airbnb.com/rooms/833990444311719408/reviews?adults=1&category_tag=Tag%3A5348&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1594712943&search_mode=flex_destinations_search&check_in=2024-03-03&check_out=2024-03-08&source_impression_id=p3_1708319472_TMgo5yGpdPKw01UD&previous_page_section_name=1000&federated_search_id=3018849f-aad7-4182-b800-0d9b233142eb'
    driver.get(url)

    # Scrape data using Selenium, 
    reviews = driver.find_elements(By.XPATH, '//div[@data-review-id]//div[2]//span')[2]
    
    reviews = [elem.text for elem in reviews]
    print(reviews)

    # Simple summary of reviews - concatenate and truncate for simplicity
    summary = ' '.join(reviews)[:500] + '...' if len(reviews) > 0 else 'No reviews found.'
    print(summary)

    # Send POST request to Flask server
    response = requests.post('http://127.0.0.1:5000', json={'summary': summary})

    # Print response from Flask application
    print(response.json())

    # Close the browser session
    driver.quit()


@app.route('/', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        #scrape data
        data = request.get_json()  # JSON data from POST request
        # Process the data
        if not data:
            return jsonify({"err": "no json received"}), 400
        print("Received post data:", data)
        return jsonify(data)
    elif request.method == 'GET':
        run_selenium()
        # Handle GET request for demo purpose
        return "selenium data init"

if __name__ == '__main__':
    app.run(debug=True)