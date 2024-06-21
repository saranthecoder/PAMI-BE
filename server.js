import express from 'express';
import dotenv from 'dotenv';
import cookieParser from 'cookie-parser';
import cors from 'cors';
import bodyParser from 'body-parser';

import router from './src/router/user.routes.js';
import pami from './src/PAMI/pami.js';
import connectToMongoDB from './src/db/connectToMongoDB.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8080;

app.use(cors({
    origin: 'http://127.0.0.1:8000',
    credentials: true
}));

app.use(express.json());
app.use(cookieParser());
app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api/user', router);
app.use('/api/pami', pami);

app.listen(PORT, () => {
    // connectToMongoDB();
    console.log(`Server is running in port ${PORT}`);
})
