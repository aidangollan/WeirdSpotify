import React, { useState } from 'react';
import spotifyLogo from '../spotify-4.png';
import { v4 as uuidv4 } from 'uuid';

const getRandomXPosition = () => Math.random() * window.innerWidth;

function FallingLogo({ delay, fallDuration, rotationDuration }) {
    const [xPosition, setXPosition] = useState(getRandomXPosition());
    
    // This function will be called when the animation iteration is complete.
    const resetPosition = () => {
      setXPosition(getRandomXPosition());
    };
    
    const style = {
      position: 'fixed',
      top: '-50px',
      left: `${xPosition}px`,
      transform: 'translateX(-50%)',
      zIndex: -1,
      animation: `waterfall_fallAndSpin ${fallDuration}s linear infinite ${delay}s`,
      willChange: 'transform',
    };
    
    return (
      <img
        src={spotifyLogo}
        alt="Spotify logo"
        style={style}
        className="falling-logo"
        onAnimationIteration={resetPosition}
      />
    );
  }

export default FallingLogo;