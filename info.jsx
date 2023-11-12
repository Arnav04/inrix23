import React, { useState } from 'react';

const ToggleContent = () => {
  const [isContentVisible, setIsContentVisible] = useState(false);

  const handleToggle = () => {
    setIsContentVisible(!isContentVisible);
  };

  const buttonStyle = {
    position: 'absolute',
    right: '1vh',
    top: '1vh',
    background:'white',
    border: '2px solid #000'
  };

  return (
    <div>
      <button style={buttonStyle} onClick={handleToggle}>   
        <img 
            src="https://media.istockphoto.com/id/1201139039/vector/about-help-info-information-properties-support-question-chat-bubble-icon-sign-more-info-logo.jpg?s=612x612&w=0&k=20&c=NLlJsH3JSo7inbzS-kpN0ZmlMFpwJQnq0neLLLBj84U="
            alt="More Info"
            style={{width:"2vw"}}
            ></img>
      </button>
      {isContentVisible && (
        <p style={{ position: 'absolute', top: '6vh', right: '0vh', width: '25vw', padding: "0.5ch", backgroundColor: 'lightgrey', border: '5px solid #000', borderRadius: '10px', color: 'black', fontSize: '18px'}}>
          HOW TO USE: To use this simply type in an address of around where you would like to park and our web-app will display the safest parking results in your area calculated through <br></br><b>     __1/(1.5(# of crimes) + (# of incidents))__</b><br></br>
          ParkShield harnesses the power of multiple APIs to enhance car security. It combines historical crime data, collision information, and natural disaster insights to recommend secure parking spots. The app ensures peace of mind by guiding users to parking locations with the lowest risk.
        </p>
      )}
    </div>
  );
};

export default ToggleContent;
