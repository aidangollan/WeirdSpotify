import React from 'react';
import SpotifyLogo from '../SpotifyLogo.png';

function NavBar() {
    return (
        <nav>
            <img src={SpotifyLogo} alt="SpotifyLogo" />
        </nav>
    );
}

export default NavBar;