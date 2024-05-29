function addLineBreaks(text) {
    // Replace all occurrences of '\n' with '<br>'
    return text.replace(/\n/g, '<br>');
}

// Define decrypt function

function sendDecryption() {

    // Declare PSSH variable
    let pssh = document.getElementById("index_pssh");

    // Declare License URL variable
    let license_url = document.getElementById("license_url");

    // Declare Proxy variable
    let proxy = document.getElementById("proxy");

    // Declare Headers variable
    let headers = document.getElementById("headers");

    // Declare JSON variable
    let json = document.getElementById("json");

    // Declare Cookies variable
    let cookies = document.getElementById("cookies");

    // Declare data variable
    let data = document.getElementById("data");

    // Declare JSON dictionary and add the values
    let json_dict = {
        'PSSH': pssh.value,
        'License URL': license_url.value,
        'Headers': headers.value,
        'JSON': json.value,
        'Cookies': cookies.value,
        'Data': data.value,
        'Proxy': proxy.value,
    }

    // Reset all the fields
    pssh.value = ''
    license_url.value = ''
    headers.value = ''
    json.value = ''
    cookies.value = ''
    data.value = ''
    proxy.value = ''

    // Set request options
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(json_dict)
    }

    // Send post request
    fetch('/', requestOptions)

        // Process return object
        .then(response => {
            return response.json()

                // Access JSON info
                .then(data => {

                    // Grab the message
                    let message = addLineBreaks(data['Message'])

                    // Make fields visible and update with message
                    document.getElementById("results").style.display = 'grid'
                    document.getElementById("decrypt_results").innerHTML = message
                })
        })
}