import React from 'react';

function LogoutButton() {
    const apiUrl = `${window.location.origin}/api/logout`;

    const handleLogoutClick = () => {
        window.location.href = apiUrl;
    };

    return (
        <button className="logout-button" onClick={handleLogoutClick}>Home</button>
    );
}

export default LogoutButton;
