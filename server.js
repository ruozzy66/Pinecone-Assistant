const express = require('express');
const path = require('path');
const { PythonShell } = require('python-shell');
require('dotenv').config();

const app = express();
app.use(express.json());

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'build')));

app.post('/api/chat', (req, res) => {
  const messages = JSON.stringify(req.body.messages);
  
  let options = {
    mode: 'text',
    pythonPath: 'python3', // or 'python' depending on your system
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: __dirname,
    args: [process.env.PINECONE_API_KEY, 'ti4-rules-assistant', messages]
  };

  PythonShell.run('chat_with_assistant.py', options, function (err, results) {
    if (err) {
      console.error('Error:', err);
      res.status(500).json({ error: 'An error occurred while processing your request.' });
    } else {
      console.log('Results:', results);
      res.json(JSON.parse(results[0]));
    }
  });
});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});