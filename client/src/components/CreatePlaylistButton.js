import React, { useState } from 'react';

function CreatePlaylistButton({ songIds }) {
    const apiUrl = `${window.location.origin}/api/create_playlist`;
    const [playlistURL, setPlaylistURL] = useState(null);

    const handleCreatePlaylistClick = async () => {
        console.log("Creating playlist...");
        console.log(songIds);
        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ song_ids: songIds }),
                credentials: 'include'
            });
    
            const data = await response.json();
            console.log("Received response:", data);
            if (data.success) {
                alert(data.message);
                setPlaylistURL(data.playlist_url);  // set the playlist URL in the state
                console.log("Received Playlist URL:", data.playlist_url);
            } else {
                alert("Failed to create playlist");
            }
        } catch (error) {
            console.error("Error creating playlist:", error);
        }
    };

    return (
        <div>
            <button className="create-playlist-button" onClick={handleCreatePlaylistClick}>Create Playlist</button>
            {playlistURL ? <a href={playlistURL} className="playlist-link" target="_blank" rel="noopener noreferrer">Go to Playlist</a> : null}
        </div>
    );
}

export default CreatePlaylistButton;
