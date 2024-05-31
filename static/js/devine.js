document.addEventListener('DOMContentLoaded', function() {
    // Get the current URL from the address bar
    var currentURL = window.location.href;

    // Set the current URL value in the paragraph
    document.getElementById('currentURL').innerText = currentURL;
    document.getElementById('currentURI').innerText = currentURL;
});