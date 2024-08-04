import dotenv from 'dotenv'
import { Kafka } from "kafkajs";


dotenv.config()

let HOST = process.env.BROKER_HOST;
console.log(`${HOST}:9092`)

const kafkaClient = new Kafka({
  clientId: "solarX",
  brokers: [`${HOST}:9092`],
});

export default kafkaClient;
