import express from 'express';
import cors from 'cors';
import path from 'path';
import { initDb } from './utils/db.js';
import videoRoutes from './routes/videoRoutes.js';
import { fileURLToPath } from 'url';

import dotenv from 'dotenv';
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


const app = express();
const port = 3002; // Change port for the video service

app.use(cors({ origin: 'http://localhost:3000' })); 

initDb().then(() => {
    console.log('Database initialized');
}).catch(err => {
    console.error('Error initializing database:', err);
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Use routes
app.use('/videos', videoRoutes);

app.listen(port, () => {
    console.log(`Video service running at http://localhost:${port}`);
});
