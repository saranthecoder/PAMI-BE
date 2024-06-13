import express from "express";
import multer from "multer";
import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import sharp from "sharp"; // Import sharp for image conversion

const router = express.Router();
const upload = multer({ dest: "/uploads/" });

const scriptDir = path.dirname(process.argv[1]);

router.post("/upload", upload.single("csvFile"), (req, res) => {
  const file = req.file;
  const algorithms = req.body.algorithms;

  // Check if the required parameters are provided
  if (!file || !algorithms) {
    return res.status(400).send("Please provide both the CSV file and algorithms.");
  }

  // Spawn a Python child process
  const pythonProcess = spawn('python', ['script.py', file.path, algorithms]);
  
  let result = '';

  // Capture Python script's stdout
  pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
    result += data.toString();
  });

  // Handle Python script exit
  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);

    // Send the result back to the client
    res.send(result);
  });
});

router.get('/get-image', (req, res) => {
  const scriptDir = path.resolve();
  const imagePath = path.join(scriptDir, 'graph.png');

  // Check if the image exists
  if (!fs.existsSync(imagePath)) {
    return res.status(404).send("Image not found.");
  }

  // Read the image file
  fs.readFile(imagePath, (err, data) => {
    if (err) {
      return res.status(500).send("Error reading image file.");
    }

    // Convert the image to JPEG format using sharp
    sharp(data)
      .jpeg()
      .toBuffer()
      .then((jpegData) => {
        // Send the converted image to the client
        res.contentType('image/jpeg');
        res.send(jpegData);
      })
      .catch((conversionErr) => {
        console.error("Error converting image:", conversionErr);
        res.status(500).send("Error converting image.");
      });
  });
});

export default router;
