import React from 'react';

function LoginPage() {
    const apiUrl = `${window.location.origin}/api/login`;

    const handleLoginClick = (isGuest) => {
        const loginUrl = `${apiUrl}?guest=${isGuest}`;
        window.location.href = loginUrl;
    };

    return (
        <div>
            <h1>Welcome to Spotify Playlist Creator</h1>
            <p>This is a work-in-progress project where I aim to create a tool capable of generating a Spotify playlist. 
                The names of the songs in the playlist will match the string you enter.</p>
            <p>Note that currently, the create playlist feature will not work for all users. 
                This is due to Spotify App Development settings.</p>
            <p>When using the app as a guest, the create playlist account 
                will create the playlist on a dummy account.</p>
            <a href='https://open.spotify.com/user/313coyywkmhso4iirxmakjettsjq'>This account can be found here</a>
            <button onClick={() => handleLoginClick(false)}>Login with Spotify</button>
            <button onClick={() => handleLoginClick(true)}>Continue as Guest</button>
        </div>
    );
}

export default LoginPage;
