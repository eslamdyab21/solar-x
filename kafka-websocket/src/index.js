import express from "express";
import kafkaConsumer from "./kafka_consumer.js";

const app = express();

const PORT = 8000;



app.listen(PORT, async () => {
    console.log(`Listiening to port ----> ${PORT}`);
    await kafkaConsumer("solarx_energy_consumer", ["solar_energy_data"]);
});