import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Search.css';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [autocompleteSuggestions, setAutocompleteSuggestions] = useState([]);
  const [searchButtonClicked, setSearchButtonClicked] = useState(false);
  const [sortedValues, setSortedValues] = useState([]);

  useEffect(() => {
    // Fetch data from output.txt
    fetch('/output.txt')
      .then(response => response.text())
      .then(data => {
        // Split the data into an array of parking lot names
        const suggestions = data.split('\n').filter(name => name.trim() !== '');
        setAutocompleteSuggestions(suggestions);

        // Log the content of autocompleteSuggestions
        console.log('autocompleteSuggestions:', suggestions);
      })
      .catch(error => console.error('Error fetching data:', error));

    // Fetch safety values from the backend when the component mounts
    fetchData();
  }, []); // Pass an empty dependency array to ensure this effect runs only once

  const fetchData = async () => {
    try {
      const response = await axios.get('/api/get_sorted_vals');
      const sortedVals = response.data;

      // Set the sorted values in state
      setSortedValues(sortedVals);

      console.log(sortedValues);
      // Now you can use sortedVals in your frontend as needed
    } catch (error) {
      console.error('Error fetching sorted values:', error);
    }
  };

  const fetchSafetyValues = async () => {
    try {
      console.log('Fetching safety values...');
      const safetyResponse = await fetch("/vals");

      if (!safetyResponse.ok) {
        throw new Error(`Failed to fetch safety values. Status: ${safetyResponse.status}`);
      }

      const safetyData = await safetyResponse.json();

      // Assuming safetyData has an array called 'vals'
      setSortedValues(safetyData.vals);

      console.log('Safety values:', safetyData.vals);
      // Now you can use safetyData.vals in your frontend as needed
    } catch (error) {
      console.error('Error fetching safety values:', error);
    }
  };

  const handleInputChange = event => {
    const inputValue = event.target.value;
    setQuery(inputValue);
  };

  const handleSubmit = event => {
    event.preventDefault();
    console.log('Search submitted for:', query);

    // Set the search button as clicked
    setSearchButtonClicked(true);

    // Fetch sorted values from the backend
    fetchData();
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSubmit}>
        <div className="bar">
          <div className="searchbar">
            <input
              type="text"
              value={query}
              onChange={handleInputChange}
              placeholder="Search Maps"
              className="search-input"
            />
            <button type="submit" className="search-button">
              <img
                src="https://cdn-icons-png.flaticon.com/512/1150/1150654.png"
                alt="Search Icon"
                style={{ height: '20px', position: 'relative', border: 0, top: '5px' }}
              />
            </button>
          </div>
        </div>
      </form>

      {/* Conditionally render drop-down menu only when the search button is clicked and there is input */}
      {searchButtonClicked && query && (
        <div className="results-container">
          <ul>
            {autocompleteSuggestions
              .filter(suggestion =>
                suggestion.toLowerCase().startsWith(query.toLowerCase())
              )
              .slice(0, 5) // Limit to 5 suggestions
              .map((result, index) => (
                <li key={index} className="result-item">
                  <span className="address">{result}</span>
                  {index <= 4 && (
                    <div className="divider-with-number">
                      <div className="divider"></div>
                      <div className="number">Safety: {sortedValues[index]}</div>
                    </div>
                  )}
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SearchBar;






// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import './Search.css';

// const SearchBar = () => {
//   const [query, setQuery] = useState('');
//   const [autocompleteSuggestions, setAutocompleteSuggestions] = useState([]);
//   const [searchButtonClicked, setSearchButtonClicked] = useState(false);

//   useEffect(() => {
//     // Fetch data from output.txt or your API endpoint
//     fetch('/output.txt')
//       .then(response => response.text())
//       .then(data => {
//         // Split the data into an array of parking lot names
//         const suggestions = data.split('\n').filter(name => name.trim() !== '');
//         setAutocompleteSuggestions(suggestions);
  
//         // Log the content of autocompleteSuggestions
//         console.log('autocompleteSuggestions:', suggestions);
//       })
//       .catch(error => console.error('Error fetching data:', error));
//   }, []);

//   const handleInputChange = (event) => {
//     const inputValue = event.target.value;
//     setQuery(inputValue);
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     console.log('Search submitted for:', query);

//     // Set the search button as clicked
//     setSearchButtonClicked(true);

//     // You can perform a search here or handle the form submission as needed
//   };
//   const fetchData = async () => {
//     try {
//         const response = await axios.get('/api/get_sorted_vals');
//         const sortedVals = response.data;
//         console.log(sortedVals);
//         // Now you can use sortedVals in your frontend as needed
//     } catch (error) {
//         console.error('Error fetching sorted values:', error);
//     }
// };
//     const dictionaryArray = Object.entries(myDictionary);
//     const firstFiveItems = dictionaryArray.slice(0, 5);

//   return (
//     <div className="search-container">
//       <form onSubmit={handleSubmit}>
//         <div className="bar">
//           <div className="searchbar">
//             <input
//               type="text"
//               value={query}
//               onChange={handleInputChange}
//               placeholder="Search Maps"
//               className="search-input"
//             />
//             <button type="submit" className="search-button">
//               <img
//                 src="https://cdn-icons-png.flaticon.com/512/1150/1150654.png"
//                 alt="Search Icon"
//                 style={{ height: '20px', position: 'relative', border:0, top: '5px' }}
//                 onclick="fetchData()"
//               />
//             </button>
//           </div>
//         </div>
//       </form>

//       {/* Conditionally render drop-down menu only when the search button is clicked and there is input */}
//       {searchButtonClicked && query && (
//         <div className="results-container">
//           <ul>
//             {autocompleteSuggestions
//               .filter(suggestion =>
//                 suggestion.toLowerCase().startsWith(query.toLowerCase())
//               )
//               .slice(0, 5) // Limit the number of results to 5
//               .map((result, index) => (
//                 <li key={index} className="result-item">
//                   <span className="address">{result}</span>
//                 {index < 4 && <div className="divider"></div>}
//                   {index === 4 && (
//                     <div className="divider-with-number">
//                       <div className="divider"></div>
//                       <div className="number">Safety: </div>
//                     </div>
//                   )}
//                   {index < 4 && <div className="divider-with-number">
//                     <div className="divider"></div>
//                     <div className="number">Safety: 10</div>
//                   </div>}
//                 </li>
//               ))}
//           </ul>
//         </div>
//       )}
//     </div>
//   );
// };



// export default SearchBar;