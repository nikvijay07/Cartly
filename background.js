<<<<<<< HEAD
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'sendURL') {
        const url = window.location.href;
        fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }
});
=======
chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content.js']
    });
  });
  
>>>>>>> ramya
