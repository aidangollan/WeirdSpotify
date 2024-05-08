import React, { useEffect, useState } from 'react';
import '../styles.css';
import FallingLogo from '../components/LogoRainfall'; 
import { v4 as uuidv4 } from 'uuid';

function LoginPage() {
    const apiUrl = `https://weirdspotify.com/api/login`;
  
    const handleLoginClick = (isGuest) => {
      const loginUrl = `${apiUrl}?guest=${isGuest}`;
      window.location.href = loginUrl;
    };
  
    const fallDuration = 10;
    const rotationDuration = 5;
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

    const [visits, setVists] = useState('...');

    useEffect(() => {
      const getVisits = async () => {
        const response = await fetch(`https://weirdspotify.com/api/getvisits`);
        const data = await response.json();
        setVists(data.visits);
        console.log("visits", data.visits);
      };
      getVisits();
    }, []);

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
            <p>{visits} Playlists and Counting!</p>
        </div>
    );
}

export default LoginPage;