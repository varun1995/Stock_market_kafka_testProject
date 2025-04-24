import threading
import time
import pandas as pd
import json
from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
from s3fs import S3FileSystem

BOOTSTRAP_SERVERS = ['51.20.95.4:9092']
TOPIC_NAME = 'demo_testing3'
GROUP_ID = 'my-combined-group'

# S3 setup
s3 = S3FileSystem()

# Load dataset once
df = pd.read_csv('indexProcessed.csv')


# ----------- PRODUCER FUNCTION -----------
def start_producer():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    print("🚀 Producer started...")
    try:
        while True:
            dict_stock = df.sample(1).to_dict(orient="records")[0]
            producer.send(TOPIC_NAME, value=dict_stock)
            print("📤 Sent:", dict_stock)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Producer stopped.")
    finally:
        producer.flush()
        producer.close()
        print("🧹 Producer connection closed.")


# ----------- CONSUMER FUNCTION -----------
def start_consumer():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    print("📡 Consumer started... Writing to S3...")

    try:
        for count, message in enumerate(consumer):
            if message.value:
                file_path = f"s3://kafka-stock-market-varun/stock_market_{count}.json"
                with s3.open(file_path, mode='w', encoding='utf-8') as file:
                    json.dump(message.value, file)
                print(f"📥 Received and written to S3: {file_path}")
    except KeyboardInterrupt:
        print("\n🛑 Consumer stopped.")
    finally:
        consumer.close()
        print("🧹 Consumer connection closed.")


# ----------- MAIN RUNNER -----------
if __name__ == '__main__':
    producer_thread = threading.Thread(target=start_producer)
    consumer_thread = threading.Thread(target=start_consumer)

    # Start both threads
    consumer_thread.start()
    time.sleep(2)  # Small delay to ensure consumer is ready
    producer_thread.start()

    # Wait for both to finish (until Ctrl+C)
    producer_thread.join()
    consumer_thread.join()
