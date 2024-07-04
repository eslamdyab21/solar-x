import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

const startWebSocketServers = async () => {
  wss.on("connection", (ws) => {
    console.log("WebSocket server connected");
  });

  wss.on("error", (error) => {
    console.error("WebSocket server error:", error);
  });

};

export { wss, startWebSocketServers };