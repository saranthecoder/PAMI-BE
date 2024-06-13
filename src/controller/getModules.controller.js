import PamiModules from "../models/pamiModules.model.js";


export const getModules = async (req,res) => {
    try {
        let modules = await PamiModules.find()      
        res.status(200).json({ modules: modules});
    } catch (error) {
        console.log("Error in getModules controller", error.message);
        res.status(500).json({ error: "Internal Server error" })

    }
}