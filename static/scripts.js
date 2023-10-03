document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(event.target);

    // Send data to server using fetch (assuming POST method and JSON response)
    fetch('/search', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    
    .then(response => response.json())
    .then(data => {
        // Assuming data.names contains the list of names
        const resultsList = document.getElementById('resultsList');
        
        // Clear existing list
        resultsList.innerHTML = '';

        // Populate the list with new results
        data.names.forEach(name => {
            const listItem = document.createElement('li');
            listItem.textContent = name;
            resultsList.appendChild(listItem);
        });

        // Scroll to results
        resultsList.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
});