import React, { useState } from 'react';

function PlaylistButton({ songIds }) {
    const [lastCreatedSongIds, setLastCreatedSongIds] = useState([]);
    const [lastCreatedPlaylistURL, setLastCreatedPlaylistURL] = useState(null);

    const apiUrl = `${window.location.origin}/api/create_playlist`;

    const handleGoToPlaylistClick = async () => {
        console.log("Checking playlist and redirecting to Spotify...");
        console.log(songIds);

        // Check if current songIds match the last created songIds
        if (JSON.stringify(songIds) === JSON.stringify(lastCreatedSongIds)) {
            window.open(lastCreatedPlaylistURL, "_blank", "noopener noreferrer");  // open the previously created Spotify playlist
            return;
        }

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
                console.log("Received Playlist URL:", data.playlist_url);
                setLastCreatedSongIds(songIds);  // Update the last created songIds
                setLastCreatedPlaylistURL(data.playlist_url);  // Update the last created playlist URL
                window.open(data.playlist_url, "_blank", "noopener noreferrer");  // open the new Spotify playlist
            } else {
                alert("Failed to create playlist");
            }
        } catch (error) {
            console.error("Error creating playlist:", error);
        }
    };

    // Check if songIds exists and is not empty before rendering the button
    if (songIds && songIds.length > 0) {
        return (
            <button className="go-to-playlist-button" onClick={handleGoToPlaylistClick}>
                View Playlist On Spotify
            </button>
        );
    } else {
        return null;  // Return nothing if songIds is empty or not provided
    }
}

export default PlaylistButton;
