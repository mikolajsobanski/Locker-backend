from kafka import KafkaProducer
from kafka import KafkaConsumer
from django.conf import settings

def send_message_to_kafka(topic, message):
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    producer.send(topic, value=message.encode('utf-8'))
    producer.flush()
    producer.close()



def consume_messages_from_kafka(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID
    )
    for message in consumer:
        # Process the received message here
        print(f"Received message: {message.value.decode('utf-8')}")
