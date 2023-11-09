import React, { useState } from 'react';
import { handleFormSubmit } from '../api';
import SpotifyLogo9 from '../spotify-9.png';
import '../styles.css';

import NavBar from '../components/NavBar';
import SearchForm from '../components/SearchForm';
import ResultsList from '../components/ResultsList';

function SearchPage() {
    const [songs, setSongs] = useState([]);
    const [errors, setErrors] = useState([]);
    const [query, setQuery] = useState('');
    const [animationState, setAnimationState] = useState('off-screen');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setAnimationState('entering-spinning'); // Start entering and spinning animation
        
        // Perform the search and wait for the result.
        const result = await handleFormSubmit(query);
    
        // Set the animation state to 'exiting' once the search is complete.
        if (Array.isArray(result.songs)) {
            setSongs(result.songs);
            setAnimationState('exiting'); // Trigger the exit animation
            // Set a timeout to change the state to 'idle' after the exit animation duration.
            setTimeout(() => setAnimationState('idle'), 1000); // Match with the duration of the exit animation
        } else {
            console.error("Received unexpected songs data format from server");
        }
    
        if (Array.isArray(result.errors)) {
            setErrors(result.errors);
        } else {
            console.error("Received unexpected errors data format from server");
        }
    };

    const modifiedSongs = songs.map((song, index) => ({
        ...song,
        frontend_id: index
    }));

    const songIds = modifiedSongs.map(song => song.id);

    console.log("songIds:", songIds);
    console.log("songs:", songs);

    return (
        <div>
            <NavBar songIds={songIds}/>
            <div className="container">
                <SearchForm 
                    query={query} 
                    onQueryChange={e => setQuery(e.target.value)}
                    onSubmit={handleSubmit}
                />
                <ResultsList songs={modifiedSongs} errors={errors} />
            </div>
            <img 
                src={SpotifyLogo9}
                className={`spotify-logo ${
                    animationState === 'entering-spinning'
                        ? 'logo-entering-spinning'
                        : animationState === 'exiting'
                        ? 'logo-exiting'
                        : 'logo-idle'
                }`} 
                alt="Spotify Logo"
            />
        </div>
    );
}

export default SearchPage;
