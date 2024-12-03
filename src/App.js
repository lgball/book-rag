import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

// Import React Bootstrap components
import {
  Container,
  Row,
  Col,
  Form,
  Button,
  Card,
  Alert,
  Spinner,
} from "react-bootstrap";

// Component for PDF Upload
function PDFUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadStatus("");
  };

  const handleFileUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      setUploadStatus("No file selected");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      setIsUploading(true);
      const response = await axios.post(
        "http://localhost:8080/upload-pdf",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setUploadStatus(`Uploaded ${file.name}`);
      onUploadSuccess();
    } catch (error) {
      setUploadStatus("Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card className="mb-4">
      <Card.Body>
        <Card.Title>Upload PDF</Card.Title>
        <Form onSubmit={handleFileUpload}>
          <Form.Group controlId="formFile" className="mb-3">
            <Form.Control type="file" accept=".pdf" onChange={handleFileChange} />
          </Form.Group>
          <Button variant="primary" type="submit" disabled={isUploading}>
            {isUploading ? <Spinner as="span" animation="border" size="sm" /> : "Upload"}
          </Button>
        </Form>
        {uploadStatus && (
          <Alert
            variant={uploadStatus.includes("Uploaded") ? "success" : "danger"}
            className="mt-3"
          >
            {uploadStatus}
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
}

// Component for PDF Selection and Deletion
function PDFSelection({ selectedPDF, onSelectPDF, onDeletePDF }) {
  const [pdfList, setPDFList] = useState([]);
  const [isDeleting, setIsDeleting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const fetchPDFList = async () => {
    try {
      const response = await axios.get("http://localhost:8080/list-pdfs");
      setPDFList(response.data.pdfs);
    } catch (error) {
      console.error("Failed to fetch PDF list");
      setErrorMessage("Failed to fetch PDF list");
    }
  };

  useEffect(() => {
    fetchPDFList();
  }, []);

  const handleDelete = async () => {
    if (!selectedPDF) {
      alert("Please select a PDF to delete.");
      return;
    }
    try {
      setIsDeleting(true);
      const response = await axios.post("http://localhost:8080/delete-pdf", {
        pdf: selectedPDF,
      });
      alert(response.data.message);
      onSelectPDF("");
      fetchPDFList();
      if (onDeletePDF) onDeletePDF();
    } catch (error) {
      console.error("Failed to delete PDF");
      alert("Failed to delete PDF");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <Card className="mb-4">
      <Card.Body>
        <Card.Title>Select PDF</Card.Title>
        {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
        <Form.Group controlId="selectPDF" className="mb-3">
          <Form.Label>Choose a PDF</Form.Label>
          <Form.Select
            value={selectedPDF}
            onChange={(e) => onSelectPDF(e.target.value)}
          >
            <option value="">Select a PDF</option>
            {pdfList.map((pdf) => (
              <option key={pdf} value={pdf}>
                {pdf}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        <Button
          variant="danger"
          onClick={handleDelete}
          disabled={isDeleting || !selectedPDF}
        >
          {isDeleting ? <Spinner as="span" animation="border" size="sm" /> : "Delete Selected PDF"}
        </Button>
      </Card.Body>
    </Card>
  );
}

// Component for LLM Chat Window with Conversation History
function LLMChatWindow({ selectedPDF }) {
  const [inputPrompt, setInputPrompt] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handlePromptSubmit = async (event) => {
    event.preventDefault();
    if (!selectedPDF) {
      alert("Please select a PDF.");
      return;
    }
    if (!inputPrompt.trim()) {
      alert("Please enter a prompt.");
      return;
    }

    const history = chatHistory.map((chat) => [chat.prompt, chat.response]);

    try {
      setIsLoading(true);
      const response = await axios.post("http://localhost:8080/chat", {
        query: inputPrompt,
        pdf: selectedPDF,
        history: history,
      });
      const responseText = response.data.response;
      setChatHistory([
        ...chatHistory,
        { prompt: inputPrompt, response: responseText },
      ]);
      setInputPrompt("");
    } catch (error) {
      console.error("Failed to get response");
      setErrorMessage("Failed to get response from the server.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="mb-4">
      <Card.Body>
        <Card.Title>Chat with LLM</Card.Title>
        <div className="chat-window mb-3"
        style={{maxHeight:"600px", overflowY: "auto"}}>
          {chatHistory.length === 0 && <p>No conversations yet.</p>}
          {chatHistory.map((chat, index) => (
            <div key={index} className="mb-2">
              <p>
                <strong>User:</strong> {chat.prompt}
              </p>
              <p>
                <strong>LLM:</strong> {chat.response}
              </p>
            </div>
          ))}
        </div>
        {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
        <Form onSubmit={handlePromptSubmit}>
          <Row>
            <Col xs={9}>
              <Form.Control
                type="text"
                value={inputPrompt}
                onChange={(e) => setInputPrompt(e.target.value)}
                placeholder="Enter your prompt"
                disabled={isLoading}
              />
            </Col>
            <Col xs={3}>
              <Button variant="primary" type="submit" disabled={isLoading}>
                {isLoading ? <Spinner as="span" animation="border" size="sm" /> : "Send"}
              </Button>
            </Col>
          </Row>
        </Form>
      </Card.Body>
    </Card>
  );
}

function App() {
  const [selectedPDF, setSelectedPDF] = useState("");
  const [newChatCounter, setNewChatCounter] = useState(0);

  const handlePDFUploadSuccess = () => {
    // You can add any additional logic here if needed after a successful upload
  };

  const handlePDFDeletion = () => {
    // Reset the selected PDF after deletion
    setSelectedPDF("");
  };

  const handleNewChat = () => {
    setSelectedPDF("");
    setNewChatCounter(prev => prev + 1);
  };

  return (
    <div className="App bg-dark text-light min-vh-100">
      <Container className="py-4">
        <header className="mb-4 d-flex justify-content-between align-items-center">
          <h1 className="text-center mb-0">Welcome to Chapter Chat!</h1>
          <Button variant="secondary" onClick={handleNewChat}>
            New Chat
          </Button>
        </header>
        <PDFUpload onUploadSuccess={handlePDFUploadSuccess} />
        <PDFSelection
          selectedPDF={selectedPDF}
          onSelectPDF={setSelectedPDF}
          onDeletePDF={handlePDFDeletion}
        />
        <LLMChatWindow key={newChatCounter} selectedPDF={selectedPDF} />
      </Container>
    </div>
  );
}

export default App;