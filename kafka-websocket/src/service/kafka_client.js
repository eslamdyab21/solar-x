import { Kafka } from "kafkajs";

const HOST = "localhost";

const kafkaClient = new Kafka({
  clientId: "solarX",
  brokers: [`${HOST}:9092`],
});

export default kafkaClient;