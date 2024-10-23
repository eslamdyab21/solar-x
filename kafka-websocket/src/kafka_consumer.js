import kafkaClient from "./service/kafka_client.js";

const kafkaConsumer = async (groupId, topics, wss) => {
  const consumer = kafkaClient.consumer({ groupId: groupId });
  await consumer.connect();
  await consumer.subscribe({ topics: topics , fromBeginning: false});

  const handleMessage = async ({ topic, message }) => {
    
    wss.clients.forEach((client) => {
      if (client.readyState === 1) {
        client.send(message.value.toString());
      }
    });
    
    console.log(
      `Topic - ${topic}, Message - ${message.value.toString()}`
    );
  };

  try {
    await consumer.run({
      eachMessage: handleMessage,
    });
  } catch (error) {
    console.error(error);
  }
};

export default kafkaConsumer;