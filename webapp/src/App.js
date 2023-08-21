// App.js
import React, { useState } from 'react';
import InputForm from './InputForm';
import ResponseDisplay from './ResponseDisplay';

function App() {
  const [response, setResponse] = useState('');
  console.log("app is displayed")
  return (
    <div>
      <h1>Enter Text:</h1>
      <InputForm setResponse={setResponse} />
      <ResponseDisplay response={response} />
    </div>
  );
}

export default App;
