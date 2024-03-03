// Listen for when the popup is opened

document.addEventListener('DOMContentLoaded', function() {
    // Send a message to the background script to request the current URL
    chrome.runtime.sendMessage({ action: 'getCurrentUrl' });
});

// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.url) {
        // Update the UI of the popup with the received URL
        document.getElementById('currentUrl').textContent = request.url;
    }
});

const generateButton = document.getElementById('generate')


generateButton.addEventListener('click', async function() {
    const text = document.getElementById('currentUrl').textContent;
    const review =  await fetch(`http://127.0.0.1:5000/?param1=${encodeURIComponent(text)}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.result);
        return data.summary 
    })
    .catch(error => {
        console.error('Error:', error);
    });


    document.getElementById('Summary').textContent = review;
})