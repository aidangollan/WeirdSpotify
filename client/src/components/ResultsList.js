import React from 'react';

function ResultsList({ songs }) {
    return (
        <div>
            <ul id="resultsList">
                {songs.map((song) => {
                    if (song.frontend_id) {
                        return <li key={song.frontend_id}>{song.name}, By: {song.artist}</li>
                    } else if (song.error) {
                        return <li key={song.error} style={{ color: 'red' }}>{song.error}</li>
                    }
                    return null;
                })}
            </ul>
        </div>
    );
}

export default ResultsList;
