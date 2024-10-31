import express from 'express';
import { authenticate } from '../utils/auth.js';
import { listVideos, uploadVideo, downloadVideo, deleteVideo, transcode } from '../controllers/videoController.js';

const router = express.Router();

// Define routes
router.get('/', authenticate, listVideos);
router.post('/upload', authenticate, uploadVideo);
router.get('/download/:id', authenticate, downloadVideo);
router.delete('/:id', authenticate, deleteVideo);
router.post('/transcode/:videoId', authenticate, transcode);

export default router;
