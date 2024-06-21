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
  const { scriptPath }= req.body;

  // Check if the required parameters are provided
  if (!file || !scriptPath ) {
    return res.status(400).send("Please provide the CSV file, script path, and algorithms.");
  }

  // Resolve the script path to an absolute path
  const resolvedScriptPath = path.resolve(scriptPath);

  // Spawn a Python child process
  const pythonProcess = spawn('python', [resolvedScriptPath, file.path]);
  
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


router.get('/get-image/:imageName', (req, res) => {
  const { imageName } = req.params;
  const scriptDir = path.resolve();
  const resultsDir = path.join(scriptDir, 'src','GRAPHS');
  const imagePath = path.join(resultsDir, imageName);

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

        

        // Delete the image file after sending
        /*
        fs.unlink(imagePath, (unlinkErr) => {
          if (unlinkErr) {
            console.error(`Error deleting image file: ${unlinkErr}`);
          }
        });
        */


      })
      .catch((conversionErr) => {
        console.error("Error converting image:", conversionErr);
        res.status(500).send("Error converting image.");
      });
  });
});


export default router;
