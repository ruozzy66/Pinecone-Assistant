const express = require('express');
const path = require('path');
const { PythonShell } = require('python-shell');
require('dotenv').config();

const app = express();
app.use(express.json());

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'build')));

app.post('/api/chat', (req, res) => {
  console.log('Received chat request:', JSON.stringify(req.body));
  const messages = JSON.stringify(req.body.messages);
  
  let options = {
    mode: 'text',
    pythonPath: 'python3',
    pythonOptions: ['-u'],
    scriptPath: __dirname,
    args: [process.env.PINECONE_API_KEY, 'ti4-rules-assistant', messages],
    timeout: 30 * 1000 // 30 seconds timeout
  };

  PythonShell.run('chat_with_assistant.py', options, function (err, results) {
    if (err) {
      console.error('Error in Python script:', err);
      return res.status(500).json({ error: 'An error occurred while processing your request.', details: err.message });
    }
    
    console.log('Python script output:', results);
    
    if (!results || results.length === 0) {
      console.log('No output from Python script.');
      return res.status(500).json({ error: 'No output from Python script.' });
    }

    try {
      const parsedResults = JSON.parse(results[0]);
      console.log('Parsed results:', parsedResults);
      res.json(parsedResults);
    } catch (parseError) {
      console.error('Error parsing Python script output:', parseError);
      res.status(500).json({ 
        error: 'An error occurred while processing the response.', 
        details: parseError.message,
        rawOutput: results[0]
      });
    }
  });
});

// CORS middleware
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
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
