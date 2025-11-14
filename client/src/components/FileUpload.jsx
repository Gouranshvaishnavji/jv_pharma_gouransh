import React, { useState } from "react";
import api from "../api/client";

function FileUpload() {
  const [files, setFiles] = useState([]);
  const [response, setResponse] = useState(null);

  const handleUpload = async () =>
    {
      const formData = new FormData();
      for (const file of files) {
        formData.append("files", file);
      }

      const res = await api.post("/docs/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResponse(res.data);
    };

  return (
    <div>
      <h3>Upload Documents</h3>
      <input
        type="file"
        multiple
        onChange={(e) => setFiles(e.target.files)}
      />
      <button onClick={handleUpload}>Upload</button>

      {response && (
        <pre style={{ background: "#eee", padding: 10 }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default FileUpload;
