import { useState } from "react";
import Tesseract from "tesseract.js"; 

const ImageUploader = ({ onImageUpload }) => {
  const [image, setImage] = useState(null);
  const [extractedText, setExtractedText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      onImageUpload(file);
      
      setLoading(true);
      try {
        const { data } = await Tesseract.recognize(file, "eng");
        setExtractedText(data.text);
      } catch (error) {
        console.error("Error extracting text:", error);
      } finally {
        setLoading(false);
      }
    }
  };

  const sendToBackend = async () => {
    if (extractedText) {
      try {
        const response = await fetch("http://localhost:5000/api/upload-text", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: extractedText }),
        });
        const result = await response.json();
        console.log("Backend Response:", result);
      } catch (error) {
        console.error("Error sending data to backend:", error);
      }
    }
  };

  return (
    <div>
      <input type="file" className="form-control mb-3" accept="image/*" onChange={handleFileChange} />
      {loading && <p className="text-center text-primary">Extracting text, please wait...</p>}
      {extractedText && (
        <div className="mt-3">
          <h5>Extracted Text:</h5>
          <textarea className="form-control mb-2" rows="4" value={extractedText} readOnly />
          <button className="btn btn-success w-100" onClick={sendToBackend}>
            Send to Backend
          </button>
        </div>
      )}
      {image && (
        <div className="text-center mt-3">
          <img src={URL.createObjectURL(image)} alt="Preview" className="img-fluid rounded" />
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
