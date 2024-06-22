import PamiAlgorithms from "../models/pamiAlgo.models.js";

export const getAlgorithms = async (req, res) => {
    try {
        const pattern = req.body.pattern;
        let algo = await PamiAlgorithms.find(); 
        res.status(200).json(algo);
    } catch (error) {
        console.log("Error in getAlgorithms controller", error.message);
        res.status(500).json({ error: "Internal Server Error" });
    }
};
