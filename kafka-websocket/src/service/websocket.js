import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });
const wss2 = new WebSocketServer({ port: 9090 });

const startWebSocketServers = async () => {
  wss.on("connection", (ws) => {
    console.log("WebSocket 1 server connected");
  });

  wss.on("error", (error) => {
    console.error("WebSocket 1 server error:", error);
  });

  wss2.on("connection", (ws) => {
    console.log("WebSocket 2 server connected");
  });

  wss2.on("error", (error) => {
    console.error("WebSocket 2 server error:", error);
  });

};

export { wss, wss2, startWebSocketServers };