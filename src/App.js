import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-3xl font-bold underline">
          You have successfully gotten to the start of Book-RAG!
        </h1>
        <img src={logo} className="App-logo" alt="logo" />
        <form action="upload-pdf">
          <input type="file" id="myFile" name="filename" accept=".pdf"></input>
          <button onclick="uploadFile()">Submit</button>
          
          const pdf = document.getElementById('myFile');

          const fileData = new FormData();
          fileData.append('pdf', pdf.files[0]);

          fetch('http://localhost:5000/upload-pdf', {
            method: 'POST',
            body: fileData
          })
        </form>
      </header>
    </div>
  );
}


async function uploadFile() {
  

  const fileData = new FormData();
  fileData.append('pdf', pdf.files[0]);

  try {
    const response = await fetch('http://localhost:5000/upload-pdf', {
      method: 'POST',
      body: fileData
    });

    const result = await response.json();
    alert(result.message);
  } catch (error) {
    console.error("Error uploading image:", error);
  }
}

export default App;
