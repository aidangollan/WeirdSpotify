import React, { useState } from 'react';
import { handleFormSubmit } from '../api';
import '../styles.css';

import NavBar from '../components/NavBar';
import SearchForm from '../components/SearchForm';
import ResultsList from '../components/ResultsList';
import LogoutButton from '../components/LogoutButton';
import CreatePlaylistButton from '../components/CreatePlaylistButton';

function SearchPage() {
    const [songs, setSongs] = useState([]);
    const [query, setQuery] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await handleFormSubmit(query);
        if (result.error) {
            console.error(result.error);
        } else {
            if (Array.isArray(result.names)) {
                setSongs(result.names);
            } else {
                console.error("Received unexpected data format from server");
            }
        }
    };

    const modifiedSongs = songs.map((song, index) => ({
        ...song,
        frontend_id: index
    }));
    
    // Use frontend_id for any frontend-specific operations, but use the regular id (Spotify ID) for backend operations.
    const songIds = modifiedSongs.map(song => song.id);

    // Log songIds and song details
    console.log("songIds:", songIds);
    console.log("songs:", songs);

    return (
        <div>
            <LogoutButton />
            <NavBar />
            <div className="container">
                <SearchForm 
                    query={query} 
                    onQueryChange={e => setQuery(e.target.value)}
                    onSubmit={handleSubmit}
                />
                <ResultsList songs={modifiedSongs} />
                <CreatePlaylistButton songIds={songIds} />
            </div>
        </div>
    );
}

export default SearchPage;
