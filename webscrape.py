from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json

app = Flask(__name__)


def run_selenium():

    # Initialize Chrome WebDriver (provide the path to your chromedriver executable)
    driver = webdriver.Chrome(executable_path='./chromedriver')

    # Navigate to the correct URL
    url = 'https://www.ebay.com/b/Jordan-1-Retro-High-OG-Chicago-Reimagined-Lost-Found-2022/15709/bn_7118597235?_trkparms=parentrq%3A952efe4518d0acda81f97e98ffff8066%7Cpageci%3A8f3d8678-c865-11ee-a864-aa2c092ca962%7Cc%3A2%7Ciid%3A1%7Cli%3A8874#UserReviews'
    driver.get(url)

    # Scrape data using Selenium
    # Adjust the XPath expression to match the review elements on the webpage
    review_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/section/section[8]/div[3]/div[2]/div/div/div/div/div/div/ul/li[1]/div/div[2]/p[2]/text()')
    reviews = [elem.text for elem in review_elements]
    print(reviews)

    # Simple summary of reviews - concatenate and truncate for simplicity
    # This is a placeholder for more sophisticated summarization logic
    summary = ' '.join(reviews)[:500] + '...' if len(reviews) > 0 else 'No reviews found.'

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
        
        # Return a response (optional)
        return {'status': 'success'}

    elif request.method == 'GET':

        run_selenium()
        # Handle GET request (e.g., render a webpage)
        # You can render HTML templates or return plain text/html responses
        return 'Hello, World!'  # Example response for GET request

if __name__ == '__main__':
    app.run(debug=True)