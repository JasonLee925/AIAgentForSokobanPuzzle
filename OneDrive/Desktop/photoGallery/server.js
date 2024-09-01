const express = require("express");
const path = require("path");
const fetch = require("node-fetch"); // Ensure you have the correct version installed
const fileupload = require("express-fileupload");
const bodyParser = require("body-parser");
const helmet = require("helmet");
const morgan = require("morgan");
require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;
const unsplashAccessKey = process.env.UNSPLASH_ACCESS_KEY;

// Path to serve static files
const staticPath = path.join(__dirname, "public");

// Middleware
app.use(express.static(staticPath));
app.use(fileupload());
app.use(bodyParser.json()); // For parsing application/json

// Add security headers with a customized CSP using Helmet
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],  // Only allow content from the same origin
      scriptSrc: ["'self'", "https://trusted-scripts.com"],  // Replace with actual trusted domains
      styleSrc: ["'self'", "https://trusted-styles.com"],
      imgSrc: ["'self'", "https://images.unsplash.com", "data:"],  // Allow Unsplash and data URIs
      connectSrc: ["'self'", "https://api.unsplash.com"],  // Allow API requests to Unsplash
      objectSrc: ["'none'"],  // Disallow plugins like Flash
      upgradeInsecureRequests: [],  // Upgrade HTTP requests to HTTPS
    },
  })
);

app.use(morgan("combined")); // Log all requests

// API route to proxy requests to Unsplash
app.get("/api/search", async (req, res) => {
  const { query = "nature", page = 1 } = req.query;
  const url = `https://api.unsplash.com/search/photos?page=${page}&query=${query}&client_id=${unsplashAccessKey}`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Fetch error:", error);
    res.status(500).json({ error: "Failed to fetch images" });
  }
});

// Route to handle image uploads
app.post("/upload", (req, res) => {
  if (!req.files || !req.files.image) {
    return res.status(400).json({ error: "No file uploaded" });
  }

  const file = req.files.image;
  if (!file.mimetype.startsWith("image/")) {
    return res.status(400).json({ error: "Only image files are allowed" });
  }

  const maxSize = 5 * 1024 * 1024; // 5 MB
  if (file.size > maxSize) {
    return res.status(400).json({ error: "File size exceeds limit of 5MB" });
  }

  const date = new Date();
  const imagename = `${date.getDate()}-${date.getTime()}-${file.name}`;
  const uploadPath = path.join(staticPath, "uploads", imagename);

  file.mv(uploadPath, (err) => {
    if (err) {
      console.error("File upload error:", err);
      return res.status(500).json({ error: "Failed to upload image" });
    }
    res.json({ imageUrl: `uploads/${imagename}` });
  });
});

// Route to handle registration
app.post("/register", (req, res) => {
  const { username, password } = req.body;

  // Here you would add code to save the user to your database
  console.log(`Registering user: ${username}, password: ${password}`);

  // For demo purposes, we are just sending a success response
  res.status(200).json({ message: "Registration successful" });
});

// Serve static files for different routes
app.get("/", (req, res) => {
  res.sendFile(path.join(staticPath, "home.html"));
});

app.get("/editor", (req, res) => {
  res.sendFile(path.join(staticPath, "editor.html"));
});

app.get("/:blog", (req, res) => {
  res.sendFile(path.join(staticPath, "blog.html"));
});

// Handle all other routes
app.use((req, res) => {
  res.status(404).json("404 Not Found");
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
