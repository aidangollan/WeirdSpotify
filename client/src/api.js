async function handleFormSubmit(query) {
    const apiUrl = `${window.location.origin}/api/search`;
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })  // Send the query as JSON
        });
        
        const data = await response.json();
        
        // Ensure that the songs and errors are arrays, defaulting to empty arrays if not
        const songs = Array.isArray(data.songs) ? data.songs : [];
        const errors = Array.isArray(data.errors) ? data.errors : [];

        // Scroll to results
        const resultsDiv = document.getElementById('resultsList');
        const position = resultsDiv.offsetTop - (window.innerHeight / 2) + (resultsDiv.offsetHeight / 2);
        window.scrollTo({ top: position, behavior: 'smooth' });

        return { songs, errors };

    } catch (error) {
        console.error("Error fetching data:", error);
        return { songs: [], errors: ["Error fetching data from the server."] };
    }
}


export { handleFormSubmit };
