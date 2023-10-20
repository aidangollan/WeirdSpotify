import React from 'react';

function ResultsList({ songs, errors }) {
    return (
        <div>
            <ul id="resultsList">
                {songs.map(song => (
                    <li key={song.frontend_id}>{song.name}, By: {song.artist}</li>
                ))}
                {errors.map((error, index) => (
                    <li key={index} style={{ color: 'red' }}>{error}</li>
                ))}
            </ul>
        </div>
    );
}


export default ResultsList;
