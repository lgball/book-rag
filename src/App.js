import logo from "./logo.svg";
import "./App.css";
import React, {useState} from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState();
  const [responseText, setResponseText] = useState('');
  const [file_text, setFileText] = useState();

  function handleChange(event) {
    setFile(event.target.files[0])
  }
  
  function handleSubmit(event) {
    event.preventDefault()
    const url = 'http://localhost:5000/upload-pdf';
    const formData = new FormData();

    if (!file) {
      setResponseText("No file selected! Please select a file!")
    }
    else {
      formData.append('file', file);
      formData.append('fileName', file.name);

      const config = {
        headers: {
          'content-type': 'multipart/form-data',
        },
      };
  
      axios.post(url, formData, config).then((response) => {
        if (response.data.error) {
          setResponseText(`File "${file.name}" was empty. Please upload a different file!`)
        } 
        else {
          setFileText(response.data.text)
          setResponseText(`File "${file.name}" was uploaded successfully!`);
        }
        
      })
        .catch((error) => {
          setResponseText(`${error.response.data.error}: File "${file.name}" was empty. Please upload a different file!`)
      });
    } 
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-3xl font-bold underline">
          You have successfully gotten to the start of Book-RAG!
        </h1>
        <img src={logo} className="App-logo" alt="logo" />
        <form onSubmit={handleSubmit}>
          <input type="file" id="myFile" name="filename" accept=".pdf" onChange={handleChange}></input>
          <button type="submit">Upload PDF</button>
        </form>
        <p>{responseText}</p>
      </header>
    </div>
  );
}

export default App;
