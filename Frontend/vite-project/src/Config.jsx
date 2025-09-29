const VITE_API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";
export const Data_Format = {
    "learn_allowChange": ["name", "status", "note"],
    "learn": ["name", "note", "status", "build_time"],
    "learnFtag": ["name", "note", "status", "build_time"],
    "tag":["id", "name"],
    "url_default":VITE_API_URL
}
export default Data_Format
