import React from 'react';
import '../styles.css';

function LoginPage() {
    const apiUrl = `${window.location.origin}/api/login`;

    const handleLoginClick = (isGuest) => {
        const loginUrl = `${apiUrl}?guest=${isGuest}`;
        window.location.href = loginUrl;
    };

    return (
        <div className="spotify-login-page">
            <h1>Welcome to Weird Spotify!</h1>
            <p>
                This project lets you do something you've probably been waiting your whole life for...
                <br/>
                <strong>turn a sentence into a Spotify Playlist!!!</strong>
                <br/>
                No matter the language, input your sentence and prepare to be amazed.
            </p>
            <button className="spotify-button guest-button" onClick={() => handleLoginClick(true)}>Let's Go!</button>
        </div>
    );
}

export default LoginPage;

//<button className="spotify-button" onClick={() => handleLoginClick(false)}>Login with Spotify (Approval Needed!)</button>