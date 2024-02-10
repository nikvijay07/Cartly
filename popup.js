document.getElementById('preferences-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const preference = document.getElementById('preference').value;
    // Save the preference to Chrome's local storage
    chrome.storage.local.set({preference: preference}, function() {
        console.log('Preference saved:', preference);
    });
});