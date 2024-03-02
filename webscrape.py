from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from transformers import pipeline
import json
from spacy.lang.en import English 

app = Flask(__name__)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
# Load the spaCy model for sentence segmentation
nlp = English()
nlp.add_pipe('sentencizer')


def run_selenium(url):
    #chrome driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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

    # Summarize all reviews
    summary_of_all_reviews = summarize_in_chunks(all_reviews_text, summarizer)
    json_summary = {'Summary': summary_of_all_reviews}
    final_data = json.dumps(json_summary)
    print("SUMMMMM :) ", summary_of_all_reviews)
    driver.execute


    # Send POST request to Flask server
    response = requests.post('http://127.0.0.1:5000', json={'summaries': summary_of_all_reviews})

    driver.quit()
    return summary_of_all_reviews



def extract_key_sentences(text, nlp, max_sentences=6):
    # Use spaCy to divide the text into sentences
    doc = nlp(text)
    sentences = list(doc.sents)
    # Here you could add logic to select the most important sentences
    #
    #
    #
    # Select the most important sentences, here simply the first few
    key_sentences = ' '.join(sentence.text for sentence in sentences[:max_sentences])
    return key_sentences #single string that contains the concatenated text of the first few sentences


def summarize_in_chunks(reviews, summarizer, chunk_size=1024, max_sentences_per_chunk=6):
    # Join all reviews into a single text if it's a list
    text = ' '.join(reviews) if isinstance(reviews, list) else reviews
    # Tokenize the text to see if it exceeds the chunk size
    tokens = summarizer.tokenizer.encode(text)
    if len(tokens) <= chunk_size:
        return summarizer(text)[0]['summary_text']

    # If the text is too long, split it and summarize the key points
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    key_points = []
    for chunk in chunks:
        key_points.append(extract_key_sentences(chunk, nlp, max_sentences_per_chunk))
    
    #summarize the concatenated key points
    key_text = ' '.join(key_points)
    return summarizer(key_text)[0]['summary_text']


@app.route('/', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        #scrape data
        data = request.get_json()  # JSON data from POST request
        url = data.body
        
        # Process the data
        if not data:
            return jsonify({"err": "no json received"}), 400  
        return jsonify(data)
    elif request.method == 'GET':
        param1 = request.args.get('param1')
        summary = run_selenium(url=param1)
        # Handle GET request for demo purpose
        return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)

