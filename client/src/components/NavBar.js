import React, { useState } from 'react';
import SpotifyLogo from '../SpotifyLogo.png';
import LogoutButton from './LogoutButton';
import PlaylistButton from './PlaylistButton';

function NavBar({ songIds }) {
    return (
        <nav>
            <img src={SpotifyLogo} alt="SpotifyLogo" />
            <div className="button-container">
                <LogoutButton />
                <PlaylistButton songIds={songIds} />
            </div>
        </nav>
    );
}

export default NavBar;