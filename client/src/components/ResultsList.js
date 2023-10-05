import React from 'react';

function ResultsList({ names }) {
    return (
        <ul id="resultsList">
            {names.map(name => (
                <li key={name}>{name}</li>
            ))}
        </ul>
    );
}

export default ResultsList;