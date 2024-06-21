import mongoose from "mongoose";

const SubPatternSchema = new mongoose.Schema({
    pattern: {
        type: String,
        required: true
    },
    files: [String],
    subPatterns: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'SubPattern'
    }]
}, { timestamps: true });

const PatternSchema = new mongoose.Schema({
    pattern: {
        type: String,
        required: true
    },
    files: [String],
    subPatterns: [SubPatternSchema]
}, { timestamps: true });

const PamiAlgorithms = mongoose.model("PamiAlgorithm", PatternSchema);
export default PamiAlgorithms;
