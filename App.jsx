import React, { useState } from 'react';
import Map from './Map';
import SearchBar from './searchbar';
import Info from './info.jsx';
import './App.css';


function App() {
  // styles
  const map_style = {
    height: '100vh',
    zIndex: '1',
  };
  const search_style = {
    position: 'absolute',
    left: '5vh',
    top: '1vh',
    zIndex: '2',
  };

  const info_style = {
    position: 'absolute',
    right: '1vh',
    top: '1vh',
    zIndex: '2',
  };


  return (
    <div className="app-container">
        <div style={map_style}>
            <Map />
        </div>
        <div style={search_style}>
            <SearchBar onSearch={(searchTerm) => console.log('Searching for:', searchTerm)} />
        </div>
        <div style={info_style}>
            <Info />
        </div>

    </div>
  );
}

export default App;

// import React from 'react';
// import Map from './Map';
// import SearchBar from './searchbar';
// import './App.css'

// function App() {
//     //styles
//     const map_style = {
//         height: '100vh', // Set the height to 100% of the viewport height
//         zIndex: "1",
//         // position:'absolute'
//     };
//     const search_style = {
//         position: 'absolute',
//         left: '5vh',
//         top: '1vh',
//         zIndex: '2',
//     }
    
//     //search bar
//     const handleSearch = (searchTerm) => {
//       // Perform your search logic here
//       console.log('Searching for:', searchTerm);
//     };
  
//     return (
//         <div className="app-container">
//             <div style={map_style}> <Map /> </div>
//             <div style={search_style}> <SearchBar onSearch={handleSearch} /> </div>
//         </div>
//     );
//     //end of search bar
//     }

// export default App;
