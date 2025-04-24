
# Real-Time Stock Market Data Pipeline with Apache Kafka and AWS

This project demonstrates a real-time data engineering pipeline that simulates stock market data using a Kafka-based architecture deployed on AWS.

---

## 🧠 Project Overview

This pipeline mimics the behavior of a real-time stock market data flow. A Python-based Kafka **producer** simulates stock trades by reading from a dataset (CSV file) and sends records to a **Kafka broker** running on an EC2 instance. A **Kafka consumer**, also in Python, reads this data and stores it in **Amazon S3** in real-time.

Once in S3, the data is picked up by an **AWS Glue Crawler**, which updates the **AWS Glue Data Catalog**, making it queryable via **Amazon Athena**.

---

## 🔧 Components Used

### ✅ Data Source
- **Dataset:** Stock market data in CSV format

### ✅ Real-Time Processing
- **Apache Kafka** on Amazon EC2 (KRaft mode)
- **Kafka Producer (Python):** Simulates stock trade messages using Pandas and Kafka-Python
- **Kafka Consumer (Python):** Writes messages to S3 using `s3fs`

### ✅ Storage and Analytics
- **Amazon S3:** Stores JSON files of real-time messages
- **AWS Glue:** Crawler updates metadata
- **AWS Glue Data Catalog:** Organizes S3 data structure
- **Amazon Athena:** Allows SQL querying of data stored in S3

---

## 🗺️ Architecture

1. CSV dataset is read and simulated as a stream by the **Kafka producer**.
2. **Kafka consumer** writes each message to **Amazon S3** as a JSON file.
3. **AWS Glue Crawler** scans S3 and updates the **Glue Data Catalog**.
4. **Amazon Athena** allows querying this data with SQL.

---

## 🚀 Getting Started

1. Start your Kafka server on EC2 (KRaft mode recommended).
2. Run `producer.py` to simulate real-time stock data.
3. Run `consumer.py` to consume data and push it to S3.
4. Set up AWS Glue Crawler and Athena to explore the data.

---

## 📦 Dependencies

- kafka-python
- pandas
- s3fs
- boto3 (optional for AWS integrations)

---

## 🧪 Sample Use Cases

- Simulate a trading dashboard
- Learn Kafka with real-world data
- Query real-time data using Athena

---

## 📌 Note

Ensure your AWS credentials are configured and your EC2 has access to S3 buckets. All network ports for Kafka (default 9092) must be open for public access if used externally.

---
