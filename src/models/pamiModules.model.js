import mongoose from "mongoose";

const getModules = new mongoose.Schema({
    moduleName:String
    //createdAt, updatedAt
},{timestamps:true})

const PamiModules = mongoose.model("PamiModule",getModules);

export default PamiModules;