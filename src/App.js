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
        Maybe add a button
      </header>
    </div>
  );
}

export default App;
