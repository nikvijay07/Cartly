from selenium import webdriver
import requests
import json

# Initialize Chrome WebDriver (provide the path to your chromedriver executable)
driver = webdriver.Chrome(executable_path='./chromedriver')

# Navigate to the website
driver.get('hhttps://www.ebay.com/b/Jordan-1-Retro-High-OG-Chicago-Reimagined-Lost-Found-2022/15709/bn_7118597235?_trkparms=parentrq%3A952efe4518d0acda81f97e98ffff8066%7Cpageci%3A8f3d8678-c865-11ee-a864-aa2c092ca962%7Cc%3A2%7Ciid%3A1%7Cli%3A8874#UserReviews')

# Scrape data using Selenium
# Adjust '.review-selector' to match the CSS selector for reviews on your target website
review_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/section/section[8]/div[3]/div[2]/div/div/div/div/div/div/ul/li[1]/div/div[2]/p[2]/text()')
reviews = [elem.text for elem in review_elements]

# Simple summary of reviews - concatenate and truncate for simplicity
# This is a placeholder for more sophisticated summarization logic
summary = ' '.join(reviews)[:500] + '...' if len(reviews) > 0 else 'No reviews found.'


# Prepare the data to send to Flask, including the summarized reviews
json_data = json.dumps(summary)
#data_to_send = {'summary': summary}
print(summary)


headers={
    'Content-type':'application/json', 
    'Accept':'application/json'
}


# Send POST request with JSON data and content type header
response = requests.post('http://127.0.0.1:5000', json=data_to_send)

# Print response from Flask application
print(response.json())

# Close the browser session
driver.quit()
