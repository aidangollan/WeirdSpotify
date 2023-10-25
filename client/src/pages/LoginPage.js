import React from 'react';

function LoginPage() {
    const apiUrl = `${window.location.origin}/api/login`;

    const handleLoginClick = (isGuest) => {
        const loginUrl = `${apiUrl}?guest=${isGuest}`;
        window.location.href = loginUrl;
    };

    return (
        <div className="spotify-login-page">
            <h1>Welcome to Weird Spotify!</h1>
            <p>This is a work-in-progress project where I aim to create a tool capable of generating a Spotify playlist. 
                The names of the songs in the playlist will match the sentence you enter.</p>
            <p>Currently you need prior approval to login and add playlists to your account.
                Others will have to use guest mode.</p>
            <p>When using the app as a guest, the create playlist account 
                will create the playlist on a dummy account.</p>
            <button className="spotify-button" onClick={() => handleLoginClick(false)}>Login with Spotify (Approval Needed!)</button>
            <button className="spotify-button guest-button" onClick={() => handleLoginClick(true)}>Continue as Guest</button>
        </div>
    );
}

export default LoginPage;
