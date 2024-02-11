from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


import requests
import json
import os

app = Flask(__name__)

def extract_text_recursive(element):
    """
    Recursively extract text from nested elements.
    """
    text = element.text.strip()
    if not text:
        # If the current element has no text, continue recursively with its children
        children = element.find_elements_by_xpath('./*')
        for child in children:
            text += ' ' + extract_text_recursive(child)
    return text



def run_selenium():

    # Get the current working directory
    current_directory = os.getcwd()

    # Set the name of the ChromeDriver executable
    chromedriver_filename = 'chromedriver'

    # Construct the path to the ChromeDriver executable
    chromedriver_path = os.path.join(current_directory, chromedriver_filename)

    # Set Chrome options
    options = Options()
    options.add_argument('--headless')  # Optional: run Chrome in headless mode

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path), options=options)

# URL of the eBay product page with reviews
    url = 'https://www.hotels.com/ho117020/the-mark-new-york-united-states-of-america/?chkin=2024-02-16&chkout=2024-02-18&destType=MARKET&destination=New%20York%2C%20New%20York%2C%20United%20States%20of%20America&expediaPropertyId=19712&latLong=40.712843%2C-74.005966&neighborhoodId=553248635976381371&pwaDialog=reviews&pwa_ts=1707615291247&referrerUrl=aHR0cHM6Ly93d3cuaG90ZWxzLmNvbS9Ib3RlbC1TZWFyY2g%3D&regionId=2621&rfrr=HSR&rm1=a2&searchId=f862831b-86c1-440b-aee6-089430b72552&selected=19712&selectedRatePlan=207770343&selectedRoomType=201540607&siteid=300000001&sort=RECOMMENDED&top_cur=USD&top_dp=835&useRewards=false&userIntent=&x_pwa=1'
    driver.get(url)

    # Scrape data using Selenium
    # Adjust the XPath expression to match the review elements on the webpage
    review_elements = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/section/div[3]/div/div[2]/div[3]/section/div[1]/div")
    
    
    
    reviews = [elem.text for elem in review_elements]
    print(reviews)

    # Simple summary of reviews - concatenate and truncate for simplicity
    summary = ' '.join(reviews)[:500] + '...' if len(reviews) > 0 else 'No reviews found.'
    print(summary)

    # Prepare the data to send to Flask, including the summarized reviews
    json_data = json.dumps({'summary': summary})

    # Send POST request with JSON data and content type header to Flask server
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = requests.post('http://127.0.0.1:5000', json=json_data, headers=headers)

    # Print response from Flask application
    print(response.json())

    # Close the browser session
    driver.quit()








@app.route('/', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        # Handle POST request (e.g., scrape data)
        # You can access POST data using request.json or request.form
        data = request.json  # JSON data from POST request
        # Process the data
        print("test1")
        print(data)
        
        return data

    elif request.method == 'GET':

        run_selenium()

        # Handle GET request (e.g., render a webpage)
        # You can render HTML templates or return plain text/html responses
        data = request.json  # JSON data from POST request
        # Process the data
        print("test1")
        print(data)
        
        return data

if __name__ == '__main__':
    app.run(debug=True)