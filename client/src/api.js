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
        
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
            const data = await response.json();

            console.log("data:", data);
            console.log("data.songs:", data.songs);
            console.log("data.error:", data.error);
            
            if (data.error) {
                console.error(data.error);
                return { error: data.error };
            } else {
                if (Array.isArray(data.songs) && data.songs.every(song => song.id && song.name && song.artist)) {
                    // Optionally, handle data.errors here if you want to display them
                    // ...

                    // Scroll to results
                    const resultsDiv = document.getElementById('resultsList');
                    const position = resultsDiv.offsetTop - (window.innerHeight / 2) + (resultsDiv.offsetHeight / 2);
                    window.scrollTo({ top: position, behavior: 'smooth' });

                    return { names: data.songs };
                } else {
                    console.error("Received unexpected data format from server.");
                    return { error: "Received unexpected data format from server." };
                }
            }
        } else {
            console.error("Received non-JSON response from the server.");
            return { error: "Received non-JSON response from the server." };
        }
    } catch (error) {
        console.error("Error fetching names:", error);
        return { error: "Error fetching names." };
    }
}

export { handleFormSubmit };
