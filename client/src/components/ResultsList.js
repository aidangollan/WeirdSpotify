import React from 'react';

function ResultsList({ songs, errors }) {
    return (
        <div>
            <ul id="resultsList">
                {songs.map(song => (
                    <li key={song.frontend_id}>
                        <img src={song.image_url} alt={song.name} style={{ width: '50px', height: '50px', marginRight: '10px' }} />
                        {song.name}, By: {song.artist}
                    </li>
                ))}
                {errors.map((error, index) => (
                    <li key={index} style={{ color: 'red' }}>{error}</li>
                ))}
            </ul>
        </div>
    );
}

export default ResultsList;