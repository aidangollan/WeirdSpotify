import React from 'react';

<<<<<<< HEAD
function ResultsList({ songs }) {
    return (
        <ul id="resultsList">
            {songs.map(song => (
                <li key={song.frontend_id}>{song.name}, By: {song.artist}</li>
=======
function ResultsList({ names }) {

    return (
        <ul id="resultsList">
            {names.map((name, index) => (
                <li key={index}>{name}</li>
>>>>>>> 439b91bda30e1a6b510410d14fad2a080e7ae9cd
            ))}
        </ul>
    );
}


export default ResultsList;