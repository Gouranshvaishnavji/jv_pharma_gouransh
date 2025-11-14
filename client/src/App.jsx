import React from "react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";

function App() {
  return (
    <div style={{ padding: 30 }}>
      <h1>Medical Document Assistant</h1>
      <FileUpload />
      <hr />
      <ChatBox />
    </div>
  );
}

export default App;
