import React from 'react';

function LogoutButton() {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/logout` || `${window.location.origin}/api/logout`;

    const handleLogoutClick = () => {
        window.location.href = apiUrl;
    };

    return (
        <button className="logout-button" onClick={handleLogoutClick}>Logout</button>
    );
}

export default LogoutButton;
