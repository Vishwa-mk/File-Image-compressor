import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setMessage("Uploading...");
      const response = await axios.post("http://127.0.0.1:5000/compress", formData, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `compressed_${file.name}`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage("File compressed and downloaded successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Compression failed.");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>File & Image Compressor</h1>
      <input type="file" onChange={handleFileChange} />
      <br /><br />
      <button onClick={handleUpload}>Upload & Compress</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
