import React, { useState, useEffect } from "react";
import io from "socket.io-client";

const App = () => {
  const [socket, setSocket] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState("Disconnected");
  const [code, setCode] = useState(""); // Tároljuk a kódot
  const [receivedCode, setReceivedCode] = useState(""); // A kód, amit a backendtől kaptunk

  useEffect(() => {
    const socket = io("http://localhost:5000", {
      transports: ["websocket"], // WebSocket kapcsolat
    });

    socket.on("connect", () => {
      setConnectionStatus("Connected");
    });

    socket.on("disconnect", () => {
      setConnectionStatus("Disconnected");
    });

    // Üzenet fogadása a backendtől
    socket.on("codeUpdate", (newCode) => {
      setReceivedCode(newCode); // Frissítjük a kódot a backend által küldött új kóddal
    });

    setSocket(socket);

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleCodeChange = (e) => {
    setCode(e.target.value); // A felhasználó által írt kód
  };

  const handleSendCode = () => {
    if (socket) {
      socket.emit("codeChange", code); // Üzenet küldése a backendnek a kóddal
    }
  };

  return (
    <div>
      <h1>Code Interview Platform</h1>
      <p>WebSocket Status: {connectionStatus}</p>

      <textarea
        value={code}
        onChange={handleCodeChange}
        placeholder="Write your code here..."
      />
      <button onClick={handleSendCode}>Send Code</button>

      <h2>Received Code from Other User</h2>
      <pre>{receivedCode}</pre>
    </div>
  );
};

export default App;
