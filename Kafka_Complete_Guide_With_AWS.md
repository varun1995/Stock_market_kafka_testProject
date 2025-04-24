
# 📊 Real-Time Stock Market Data Engineering Pipeline with Kafka and AWS

This guide walks you through building a real-time data pipeline using **Apache Kafka**, **AWS EC2**, **S3**, **Glue**, and **Athena**. You will simulate live stock data with Python, stream it through Kafka, and store it on S3 for querying using Athena.

---

## 🧱 Prerequisites

Before you begin:
- ✅ An AWS account
- ✅ Basic understanding of Linux and Python
- ✅ AWS CLI configured (optional but useful)
- ✅ Python 3 environment on your local machine
- ✅ EC2 instance (Amazon Linux or Ubuntu) with internet access

---

## ⚙️ Step-by-Step Setup Guide (First-Time Setup)

### 1. 🚀 Launch EC2 and SSH In
- Launch a **t2.micro or t3.small EC2 instance** (Amazon Linux recommended)
- Allow inbound access to port **9092** (Kafka) and **22** (SSH)
- Connect to your instance:
```bash
ssh -i your-key.pem ec2-user@<YOUR_EC2_PUBLIC_IP>
```

---

### 2. 🛠️ Install Java & Kafka (KRaft Mode)
```bash
sudo yum update -y
sudo yum install java-1.8.0 -y
wget https://downloads.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz
tar -xvzf kafka_2.13-4.0.0.tgz
cd kafka_2.13-4.0.0
```

---

### 3. ⚡ Format Kafka Storage (One-Time Only)
```bash
bin/kafka-storage.sh format -t $(bin/kafka-storage.sh random-uuid) -c config/kraft/broker.properties
```

---

### 4. 🛠️ Edit `broker.properties` for Public Access
```bash
nano config/kraft/broker.properties
```
Update:
```
advertised.listeners=PLAINTEXT://<YOUR_EC2_PUBLIC_IP>:9092
log.dirs=/home/ec2-user/kafka-logs
```

---

### 5. ✅ Start Kafka Server
```bash
export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
bin/kafka-server-start.sh config/kraft/broker.properties
```
**Leave this terminal open.**

---

### 6. ✅ Create Your Kafka Topic (from another SSH tab)
```bash
cd kafka_2.13-4.0.0
bin/kafka-topics.sh --create --topic demo_testing2 --bootstrap-server <YOUR_EC2_PUBLIC_IP>:9092 --partitions 1 --replication-factor 1
```

---

## 🐍 Python Setup (On Your Local Machine)

### 1. Create a virtual environment and install packages:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install kafka-python pandas s3fs boto3
```

### 2. Create `producer.py` and `consumer.py`

**producer.py** – Simulates and sends stock data to Kafka  
**consumer.py** – Listens to Kafka and writes data to S3 in real-time

> These files should include threading to run both in a single script. You can copy from the combined version shared earlier.

---

## 📦 GitHub Integration

If you're maintaining this project on GitHub:
- Push your local folder using:
```bash
git init
git remote add origin https://github.com/your-username/kafka-stock-market-pipeline.git
git add .
git commit -m "Initial commit"
git push -u origin main
```
- Use this markdown as your `README.md`.

---

## 🧠 AWS Glue Setup

### Step 1: Create a Crawler
1. Go to AWS Glue → Crawlers → **Add crawler**
2. Set the S3 path to: `s3://kafka-stock-market-varun/`
3. Choose an IAM role with Glue & S3 access.
4. Set schedule as **On demand**
5. Choose or create a database like `stock_market_db`
6. Run the crawler

---

## 🔎 Athena Setup

### Step 2: Run Athena Query
Once the crawler updates the schema:
```sql
SELECT * FROM "stock_market_db"."stock_market_varun"
LIMIT 10;
```

Make sure Athena is pointing to the correct **query result location** in S3.

---

## 🔁 What To Do After EC2 Reboot

You **do NOT** need to re-install anything.

Just do:

1. SSH into EC2:
```bash
ssh -i your-key.pem ec2-user@<NEW_EC2_PUBLIC_IP>
```

2. Update `advertised.listeners`:
```bash
nano kafka_2.13-4.0.0/config/kraft/broker.properties
# Change IP in advertised.listeners
```

3. Start Kafka:
```bash
cd kafka_2.13-4.0.0
export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
bin/kafka-server-start.sh config/kraft/broker.properties
```

---

## ❌ What You Don’t Need to Do Again

| Action                      | Required? | Notes |
|-----------------------------|-----------|-------|
| Reformat Kafka storage      | ❌ No      | Only needed once at setup |
| Reinstall Kafka             | ❌ No      | Already configured |
| Recreate topic              | ❌ No      | Topic is persistent |
| Reconfigure everything      | ❌ No      | Except `advertised.listeners` if IP changes |

---

## 🧼 Common Mistakes to Avoid

- ❌ Running producer before Kafka is live  
- ❌ Forgetting to flush the producer  
- ❌ Using invalid JSON (single quotes)  
- ❌ Not opening port 9092 in EC2 Security Group  
- ❌ Not setting up S3 permissions for `s3fs`  
- ❌ Not using `auto_offset_reset='earliest'` in your consumer

---

## 💡 Pro Tip: Use Elastic IP
Attach a static **Elastic IP** to your EC2 so you don’t need to update `broker.properties` after each reboot.

---

## ✅ You're Done!

You now have a fully working real-time streaming data pipeline:
- From CSV → Kafka → Python → S3 → Glue → Athena → SQL dashboarding!

Happy Building! 🛠️
