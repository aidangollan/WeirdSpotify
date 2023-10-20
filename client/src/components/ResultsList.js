import React from 'react';

function ResultsList({ songs }) {
    return (
        <ul id="resultsList">
            {songs.map(song => (
                <li key={song.id}>{song.name} by {song.artist}</li>
            ))}
        </ul>
    );
}

export default ResultsList;