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

    const songIds = songs.map(song => song.id);

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
                <ResultsList songs={songs} />
                <CreatePlaylistButton songIds={songIds} />
            </div>
        </div>
    );
}

export default SearchPage;
