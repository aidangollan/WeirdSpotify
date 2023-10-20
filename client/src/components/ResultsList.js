import React from 'react';

function ResultsList({ songs }) {
    return (
        <ul id="resultsList">
            {songs.map(song => (
                <li key={song.frontend_id}>{song.name}, By: {song.artist}</li>
            ))}
        </ul>
    );
}

export default ResultsList;