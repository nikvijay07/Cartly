from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

def get_data_with_selenium(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    elements = driver.find_elements(By.CSS_SELECTOR, '.example-class')  # Adjust your CSS selector
    data = [element.text for element in elements]
    driver.quit()
    return data

@app.route('/api/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    scraped_data = get_data_with_selenium(url)
    return jsonify({"scrapedData": scraped_data})

if __name__ == '__main__':
    app.run(debug=True)
