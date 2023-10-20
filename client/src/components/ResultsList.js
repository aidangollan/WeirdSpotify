import React from 'react';

function ResultsList({ names }) {
    return (
        <ul id="resultsList">
            {names.map(song => (
                <li key={song.id}>
                    {song.name} by {song.artist}
                </li>
            ))}
        </ul>
    );
}

export default ResultsList;