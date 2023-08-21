// InputForm.js
import React, { useState } from 'react';
import axios from 'axios'; // Import Axios for making API calls

function InputForm({ setResponse }) {
  const [inputText, setInputText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    /* Posting to our `/process` endpoint with our user input 
     * TODO: get post info & cleanup */
    try {
        const apiUrl = 'http://127.0.0.1:5000/process'; 
        const response = axios.post(apiUrl, { text: inputText }); 
        response.then(result => {
            if (result && result.data) {
                setResponse(result.data);
            }
        })
      } catch (error) {
        console.error('Error fetching data:', error);
      }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  );
}

export default InputForm;
