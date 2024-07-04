import kafkaClient from "./service/kafka_client.js";

const kafkaConsumer = async (groupId, topics) => {
  const consumer = kafkaClient.consumer({ groupId: groupId });
  await consumer.connect();
  await consumer.subscribe({ topics: topics , fromBeginning: false});

  const handleMessage = async ({ topic, message }) => {
    
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