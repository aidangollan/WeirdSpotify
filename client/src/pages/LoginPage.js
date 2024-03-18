import React, { useState } from 'react';
import '../styles.css';
import FallingLogo from '../components/LogoRainfall'; 
import { v4 as uuidv4 } from 'uuid'; // Import the uuid function

function LoginPage() {
    const apiUrl = `http://127.0.0.1:5000/api/login`;
  
    const handleLoginClick = (isGuest) => {
      const loginUrl = `${apiUrl}?guest=${isGuest}`;
      window.location.href = loginUrl;
    };
  
    // Define the fall and rotation durations
    const fallDuration = 10; // Duration of the fall animation in seconds
    const rotationDuration = 5; // Duration of the rotation animation in seconds
    const logosCount = 35;
    const delayIncrement = fallDuration / logosCount;
  
    const [logos] = useState(() => 
      Array.from({ length: logosCount }, (_, index) => (
        <FallingLogo
          key={uuidv4()}
          delay={index * delayIncrement}
          fallDuration={fallDuration}
          rotationDuration={rotationDuration}
        />
      ))
    );

    return (
        <div className="spotify-login-page">
            {logos}
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