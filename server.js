app.post('/api/chat', (req, res) => {
  console.log('Received chat request:', JSON.stringify(req.body));
  const messages = JSON.stringify(req.body.messages);
  
  let options = {
    mode: 'text',
    pythonPath: 'python3',
    pythonOptions: ['-u'],
    scriptPath: __dirname,
    args: [process.env.PINECONE_API_KEY, 'ti4-rules-assistant', messages]
  };

  PythonShell.run('chat_with_assistant.py', options, function (err, results) {
    if (err) {
      console.error('Error in Python script:', err);
      res.status(500).json({ error: 'An error occurred while processing your request.' });
    } else {
      console.log('Python script output:', results);
      try {
        const parsedResults = JSON.parse(results[0]);
        res.json(parsedResults);
      } catch (parseError) {
        console.error('Error parsing Python script output:', parseError);
        res.status(500).json({ error: 'An error occurred while processing the response.' });
      }
    }
  });
});