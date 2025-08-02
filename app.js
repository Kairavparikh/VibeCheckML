
/*const express = require('express');
const cors = require('cors');
const { execFile } = require('child_process');
const path = require('path');

const app = express();
const port = 5500;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

app.post('/analyze', (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'No URL provided' });

  let videoId;
  try {
    videoId = new URL(url).searchParams.get('v');
  } catch {
    return res.status(400).json({ error: 'Invalid URL' });
  }
  if (!videoId) return res.status(400).json({ error: 'No video ID found in URL' });

  const pythonScriptPath = path.join(__dirname, 'fetch_comments.py');

  execFile('python3', [pythonScriptPath, videoId], { timeout: 15000 }, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: 'Python script failed' });
    }

    try {
      const result = JSON.parse(stdout);
      res.json({ videoId, comments: result.comments || [] });
    } catch {
      res.status(500).json({ error: 'Invalid JSON returned by Python script' });
    }
  });
});

app.listen(port, () => {
  console.log(`Server has started on http://localhost:${port}`);
});

*/