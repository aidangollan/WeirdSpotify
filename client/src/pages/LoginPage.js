import React from 'react';

function LoginPage() {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/login` || `${window.location.origin}/api/login`;

    const handleLoginClick = () => {
        // Redirect to the /login route of your Flask app
        window.location.href = apiUrl;
    };

    return (
        <div>
            <h1>Welcome to Spotify Playlist Creator</h1>
            <button onClick={handleLoginClick}>Login with Spotify</button>
        </div>
    );
}

export default LoginPage;
