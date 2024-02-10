from selenium import webdriver
import requests

# Initialize Chrome WebDriver (provide the path to your chromedriver executable)
driver = webdriver.Chrome(executable_path='./chromedriver')

# Navigate to the website
driver.get('https://www.google.com/')

# Scrape data using Selenium
# ...

headers={
    'Content-type':'application/json', 
    'Accept':'application/json'
}

# Send scraped data to Flask application
data_to_send = {'key': 'value'}  # Modify as needed

# Send POST request with JSON data and content type header
response = requests.post('http://127.0.0.1:5000', json=data_to_send)

# Print response from Flask application
print(response.json())

# Close the browser session
driver.quit()
