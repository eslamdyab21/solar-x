import express from "express";
import kafkaConsumer from "./kafka_consumer.js";
import { wss, wss2, startWebSocketServers } from "./service/websocket.js";


const PORT = 8000;
const app = express();


app.listen(PORT, async () => {
    console.log(`Listiening to port ----> ${PORT}`);

    await startWebSocketServers();
    await kafkaConsumer("solarx_energy_consumer", ["solar_energy_data"], wss);
    await kafkaConsumer("home_energy_consumer", ["home_energy_consumption"], wss2);
});