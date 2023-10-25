import React, { useState } from 'react';
import { handleFormSubmit } from '../api';
import '../styles.css';

import NavBar from '../components/NavBar';
import SearchForm from '../components/SearchForm';
import ResultsList from '../components/ResultsList';

function SearchPage() {
    const [songs, setSongs] = useState([]);
    const [errors, setErrors] = useState([]);
    const [query, setQuery] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await handleFormSubmit(query);
        
        if (Array.isArray(result.songs)) {
            setSongs(result.songs);
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
        </div>
    );
}

export default SearchPage;
