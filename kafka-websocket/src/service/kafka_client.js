import { Kafka } from "kafkajs";

require('dotenv').config();

const HOST = process.env.BROKER_HOST;

const kafkaClient = new Kafka({
  clientId: "solarX",
  brokers: [`${HOST}:9092`],
});

export default kafkaClient;