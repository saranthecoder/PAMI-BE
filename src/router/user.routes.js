import express from 'express';
import { logInUser, logOutUser, signUpUser } from '../controller/user.controller.js';
// import UserProtectingRouter from '../middleware/userProtectingRouter.js'
import { getAlgorithms } from '../controller/getAlgo.controller.js';
import { getModules } from '../controller/getModules.controller.js';

const router  = express.Router();

router.post('/signupUser', signUpUser);  // ✅

router.post('/loginUser', logInUser);  // ✅

router.get('/logoutUser', logOutUser);  // ✅

//router.get('/getModules', getModules); 

router.get('/getAlgorithms', getAlgorithms); 


export default router;