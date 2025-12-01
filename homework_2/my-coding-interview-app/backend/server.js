const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const cors = require("cors");

const app = express();
const server = http.createServer(app);

// Socket.IO konfigurálása CORS-szal
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000", // A frontend URL-je
    methods: ["GET", "POST"],
    allowedHeaders: ["my-custom-header"],
    credentials: true
  }
});

// CORS middleware a HTTP kérésekhez
app.use(cors({
  origin: "http://localhost:3000",  // A frontend URL-je
  methods: ["GET", "POST"],
  credentials: true
}));

// WebSocket kapcsolat kezelése
let currentCode = ""; // A legutóbb küldött kód

io.on("connection", (socket) => {
  console.log("User connected");

  // Küldjük a legutóbbi kódot az új csatlakozónak
  socket.emit("codeUpdate", currentCode);

  // Üzenet fogadása a frontendtől
  socket.on("codeChange", (newCode) => {
    currentCode = newCode; // Frissítjük a kódot
    io.emit("codeUpdate", currentCode); // Minden csatlakozott felhasználónak küldjük a friss kódot
  });

  socket.on("disconnect", () => {
    console.log("User disconnected");
  });
});

// Backend szerver indítása
server.listen(5000, () => {
  console.log("Server is listening on port 5000");
});
