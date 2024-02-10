
// Content script of your Chrome extension
// Event listener to capture user clicks on the webpage
document.addEventListener('click', function(event) {
    // Check if the clicked element meets your criteria
    if (event.target.matches('YOUR_ELEMENT_SELECTOR')) {
        // Send message with the sendURL action to the background script
        chrome.runtime.sendMessage({ action: 'sendURL' });
    }
});
