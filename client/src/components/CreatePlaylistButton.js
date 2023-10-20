import React from 'react';

function CreatePlaylistButton({ songIds }) {
    const apiUrl = `${window.location.origin}/api/create_playlist`;

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
            if (data.success) {
                alert(data.message);
            } else {
                alert("Failed to create playlist");
            }
        } catch (error) {
            console.error("Error creating playlist:", error);
        }
    };

    return (
        <button onClick={handleCreatePlaylistClick}>Create Playlist</button>
    );
}

export default CreatePlaylistButton;
