import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public'))); // Serve static files from public

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html')); // Serve the main HTML file
});

app.listen(PORT, () => {
    console.log(`Frontend server running at http://localhost:${PORT}`);
});
