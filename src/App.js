//import logo from "./ChapterChatLogo.png";
// import Form from "react-bootstrap/Form";
// import { InputGroup } from "react-bootstrap";
import "./App.css";
import React, { useState, useEffect } from "react";
import axios from 'axios';

function UserPrompt() {
  const [inputValue, setInputValue] = useState("");
  const [submittedPrompt, setSubmittedPrompt] = useState("");

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmittedPrompt(inputValue); // Display the submitted prompt
    setInputValue(""); // Clear the input field after submission
  };

  return (
    <div className="min-w-[550px] grid flex gap-2">
      <form onSubmit={handleSubmit}>
        <div className="flex gap-2 w-full grow">
          <input
            type="text"
            id="first_name"
            value={inputValue}
            onChange={handleInputChange}
            class="w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Input Prompt"
            required
          />

          <button
            type="submit"
            class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            Submit
          </button>
        </div>
      </form>
      {/* Display the submitted prompt */}
      <div>
        {submittedPrompt && (
          <div className="text-right mt-4 text-blue-700 p-2 rounded-lg">
            <p className="max-w-72 break-words inline-block text-md font-semibold px-2 py-1 rounded-lg bg-gray-300 text-blue-600">
              {submittedPrompt}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

function MachineResponse() {
  const [llmResponse, setLlmResponse] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {

    const timer = setTimeout(() => {
      setIsLoading(false); 
      setLlmResponse("I love responding to humans"); 
    }, 2000);

    return () => clearTimeout(timer);
  }, [llmResponse]);

  return (
      <div>
        <div className="text-left mt-4 text-gray p-2 rounded-lg">
          {isLoading ? (<div class="loading">
          <span>.</span>
          <span>.</span>
          <span>.</span>
          </div> ) : (
          <p className="max-w-72 break-words inline-block text-md font-semibold px-2 py-1 rounded-lg bg-blue-700 text-gray-300">
            {llmResponse}
          </p>
          )}
        </div>
      </div>
  );
}


  function FileUpload() {
    const [file, setFile] = useState();
    const [responseText, setResponseText] = useState('');
    const [file_text, setFileText] = useState("");

    const handleFileChange=(event)=> {
      setFile(event.target.files[0])
    }

    const handleFileSubmit = (event) => {
      event.preventDefault()

      // may need to change port to a different number to match the flask port depending on system
      const url = 'http://localhost:8080/upload-pdf';
      const formData = new FormData();

      if (!file) {
        setResponseText("No file selected! Please select a file!")
        setFileText("")
      }
      else if (file.type !== 'application/pdf') {
        setResponseText(`Incompatible File:  ${file.name} is not a pdf. Please select a PDF!`)
        setFileText("")
      }
      else {
        formData.append('file', file);
        formData.append('fileName', file.name);

        const config = {
          headers: {
            'content-type': 'multipart/form-data',
            'Access-Control-Allow-Origin': '*'
          },
        };
    
        axios.post(url, formData, config).then((response) => {

          if (response.data.text) {
            setFileText(response.data.text);
            setResponseText(`File "${file.name}" was uploaded successfully! Here is the file text:\n`);
          }
          else {
            setFileText(response.data.error)
          }
        }
        )
          .catch((error) => {
            if (error.response) {
              setResponseText(`"${error.response.data}`)
              setFileText("")
            }
        
            else {
              setResponseText(`Failed to upload file.`)
              setFileText("")
            }
        });
      } 
    }

    return (
      <div className="file-submit-button">
        <form onSubmit={handleFileSubmit}>
            <input type="file" id="myFile" name="filename" accept=".pdf" onChange={handleFileChange}></input>
            <button class='text-blue-500 bg-white hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-white-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center  hover:bg-gray-800 focus:ring-4 focus:outline-none focus:ring-white-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center light:hover:bg-gray-700 dark:focus:ring-blue-800' 
            type="submit">Upload PDF</button>
        </form>
        <div class='text-white'>
          <p>{responseText}</p>
          <p>{file_text}</p>
        </div>
      </div>
    );
  }

  function App() {
  return (
    <div className="App bg-cyan-200 2-300">
      <header className="App-header bg-white-200">
        <h1 className="text-3xl font-bold underline">
          You have successfully gotten to the start of ChapterChat!
        </h1>
      </header>
      <div className="grid flex justify-center gap-2 w-200">
        {/* <img src={logo} alt="logo" class="max-w-xs" /> */}
  
        <UserPrompt />
        <FileUpload/>
      </div>
    </div>
  );
}

export default App;
