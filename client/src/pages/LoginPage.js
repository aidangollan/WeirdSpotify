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
            <p>This project allows you to do what you've always wanted to but never could</p>
            <br />
            <p>Turn a sentence into a Spotify Playlist!!</p>
            <br />
            <p>Enter any sentence, in any language, then watch the magic happen!</p>
            <button className="spotify-button guest-button" onClick={() => handleLoginClick(true)}>Lets Go!</button>
        </div>
    );
}

export default LoginPage;

//<button className="spotify-button" onClick={() => handleLoginClick(false)}>Login with Spotify (Approval Needed!)</button>