import { uploadFile, listFiles, downloadFile, deleteFile, transcodeVideo } from '../utils/fileUtils.js';
import { authenticate } from '../utils/auth.js';

export const listVideos = (req, res) => listFiles(req, res);
export const uploadVideo = (req, res) => uploadFile(req, res);
export const downloadVideo = (req, res) => downloadFile(req, res);
export const deleteVideo = (req, res) => deleteFile(req, res);
export const transcode = (req, res) => transcodeVideo(req, res);
