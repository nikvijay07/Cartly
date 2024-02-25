// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//     if (message.action === 'sendURL') {
//         const url = window.location.href;
//         fetch('http://127.0.0.1:5000/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ url: url })
//         })
//         .then(response => response.json())
//         .then(data => console.log(data))
//         .catch(error => console.error('Error:', error));
//     }
// });


// Listen for messages from popup script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'getCurrentUrl') {
        // Send the current URL to the popup script
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            const currentUrl = tabs[0].url;
            chrome.runtime.sendMessage({ url: currentUrl });
        });
    }
});
