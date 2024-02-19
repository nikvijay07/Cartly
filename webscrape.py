from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests

app = Flask(__name__)

def run_selenium():
    #chrome driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'https://www.airbnb.com/rooms/833990444311719408/reviews?adults=1&category_tag=Tag%3A5348&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1594712943&search_mode=flex_destinations_search&check_in=2024-03-03&check_out=2024-03-08&source_impression_id=p3_1708319472_TMgo5yGpdPKw01UD&previous_page_section_name=1000&federated_search_id=3018849f-aad7-4182-b800-0d9b233142eb'
    driver.get(url)

    # Wait for the elements to be loaded
    wait = WebDriverWait(driver, 10)
    review_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-review-id]')))

    #put all reviews into list
    all_reviews_text = []
    for review_element in review_elements:
        spans = review_element.find_elements(By.TAG_NAME, 'span')
        if len(spans) > 6:
            all_reviews_text.append(spans[6].text)
            print(spans[6].text)
        else:
            print("Review (7th span) not found")

    # Send POST request to Flask server
    response = requests.post('http://127.0.0.1:5000', json={'summary': all_reviews_text})

    driver.quit()


@app.route('/', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        #scrape data
        data = request.get_json()  # JSON data from POST request
        # Process the data
        if not data:
            return jsonify({"err": "no json received"}), 400
        # print("Received post data:", data)
        return jsonify(data)
    elif request.method == 'GET':
        run_selenium()
        # Handle GET request for demo purpose
        return "selenium init"

if __name__ == '__main__':
    app.run(debug=True)