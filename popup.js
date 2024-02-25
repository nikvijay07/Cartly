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
