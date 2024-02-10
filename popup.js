document.getElementById('scrapeButton').addEventListener('click', function() {
    const urlToScrape = document.getElementById('urlToScrape').value;
    fetch('http://localhost:5000/api/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: urlToScrape }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('scrapedData').textContent = JSON.stringify(data.scrapedData);
    })
    .catch(error => console.error('Error:', error));
});