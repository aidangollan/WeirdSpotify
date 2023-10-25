import React from 'react';

function SearchForm({ query, onQueryChange, onSubmit }) {
    return (
        <form onSubmit={onSubmit}>
            <label htmlFor="query">Enter Your Sentence Here!</label>
            <input
                type="text"
                id="query"
                value={query}
                onChange={onQueryChange}
                placeholder="Enter your sentence here..."
                required
            />
            <input type="submit" value="Create Playlist" />
        </form>
    );
}

export default SearchForm;