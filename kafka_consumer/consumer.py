from cel_main import sentiment_task

import os
from json import loads

from kafka import KafkaConsumer
from kafka import TopicPartition , OffsetAndMetadata

kafka_broker = os.getenv("KAFKA_BROKER")
topic = os.getenv("KAFKA_TOPIC")
consumer_group_id = os.getenv("CONSUMER_GROUP")

consumer = KafkaConsumer(topic, bootstrap_servers=kafka_broker, group_id=consumer_group_id,
                        value_deserializer= lambda x: loads(x.decode('utf-8')),
                        fetch_min_bytes=150,
                        fetch_max_wait_ms=5000,
                        auto_offset_reset='earliest',
                        enable_auto_commit =False)


if __name__ == "__main__":
    for message in consumer:
        print(f"Received message")
        data = message.value
        print(f"Received data: {data}")
        sentence = data.get('sentence')
        sentiment_task.delay(sentence)
        tp=TopicPartition(message.topic,message.partition)
        om = OffsetAndMetadata(message.offset+1, message.timestamp)
        consumer.commit({tp:om})