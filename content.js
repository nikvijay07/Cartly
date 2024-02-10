chrome.storage.local.get('preference', function(data) {
    const preference = data.preference;
    if (preference) {
        const message = `Based on your preference, check out our ${preference} products!`;
        const recommendationsDiv = document.createElement('div');
        recommendationsDiv.setAttribute('style', 'position: fixed; bottom: 20px; right: 20px; background-color: white; padding: 10px; box-shadow: 0px 0px 5px rgba(0,0,0,0.2); z-index: 1000;');
        recommendationsDiv.textContent = message;
        document.body.appendChild(recommendationsDiv);
    }
});
