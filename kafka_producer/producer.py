import os
import time
from json import dumps

import schedule
from faker import Faker
from kafka import KafkaProducer
from kafka.errors import TopicAlreadyExistsError
from kafka.admin import KafkaAdminClient, NewTopic

# Access environment variables
kafka_broker = os.getenv("KAFKA_BROKER")
topic = os.getenv("KAFKA_TOPIC")
faker = Faker()

producer = KafkaProducer(bootstrap_servers=kafka_broker, 
                        value_serializer= lambda x: dumps(x).encode('utf-8'))


def create_topics(topic):
    admin_client = KafkaAdminClient(bootstrap_servers=kafka_broker)
    existing_topics = admin_client.list_topics()
    topic_list = []

    if topic not in existing_topics:
        topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))

    try:
        if topic_list:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print("Topic Created Successfully")
    except TopicAlreadyExistsError as e:
        print("Topic Already Exist")
    except  Exception as e:
        print(e)
    finally:
        admin_client.close()

def on_send_success(record_metadata,message):
    print(f"""Successfully produced '{message}' to topic {record_metadata.topic} 
          and partition {record_metadata.partition} at offset {record_metadata.offset}""")
    

def on_send_error(excp,message):
    print(f"Failed to write the message '{message}' , error : {excp}")


def gen_data():
    message = {'sentence' : faker.sentence()}
    producer.send(topic=topic, value=message).add_callback(on_send_success,message=message).add_errback(on_send_error,message=message)
    print("Sent the message {} using send method".format(message))
    producer.flush()    

if __name__ == '__main__':  
    create_topics(topic=topic)
    schedule.every(2).seconds.do(gen_data)  
    
    while True:
        schedule.run_pending()
        time.sleep(5)  # Sleep to prevent busy-waiting
      

