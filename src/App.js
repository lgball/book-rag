import logo from "./ChapterChatLogo.png";
// import Form from "react-bootstrap/Form";
// import { InputGroup } from "react-bootstrap";
import "./App.css";
import React, { useState } from "react";

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
      </div>
    </div>
  );
}

export default App;
