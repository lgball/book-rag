const express = require('express');
const path = require('path');
const app = express();

// Middleware to parse form data (needed to parse req.body in POST requests)
app.use(express.urlencoded({ extended: true }));

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Define a route to handle form submission from the login page, redirect to homepage
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // Simple example of authentication logic
  if (username === 'user' && password === 'password') {
    res.send(`Logged in as ${username}`);
  } else {
    res.send('Invalid credentials');
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
