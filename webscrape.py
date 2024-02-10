from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scrape():
    # Receive data from Selenium script
    data = request.json
    
    # Process data (e.g., scrape website)
    # ...

    # Return scraped data as response
    print("hello")
    return {'result': 'Scraped data'}

if __name__ == '__main__':
    app.run(debug=True)
