# **Kafka to MongoDB Stream – Logistics Data**

Welcome to the Kafka to MongoDB Stream Project repository! 
This project demonstrates a real-time data streaming pipeline for logistics data using Kafka, Schema Registry, Docker, and MongoDB. It highlights important data engineering practices such as data ingestion, schema enforcement, deduplication, cleansing, and scalable consumer groups.

⸻

# **🏗️ Data Architecture**

**The architecture is designed for real-time logistics data streaming:**

	1.	CSV Source – delivery_trip_truck_data.csv serves as the raw logistics dataset.
	2.	Kafka Producer – Reads data from CSV and publishes messages to a Kafka topic.
	3.	Schema Registry & Clustering – Ensures message schema consistency and scalable Kafka deployment.
	4.	Kafka Consumers (via Docker) – A consumer group with multiple instances applies filtration and cleansing rules before storing the data.
	5.	MongoDB (LogisticsDB) – Final storage, containing the truck_data collection, with deduplication (no duplicate IDs).
	6.	Confluent Sink Connector – Used for Kafka → MongoDB integration from Confluent Kafka UI.

# **Project Overview**

**This project involves:**

	1.	Producer Code – Reads from the logistics CSV and pushes records into Kafka.
	2.	Schema Registry Setup – Manages message schemas for consistency.
	3.	Consumer Code – Applies data cleansing, filtering, and deduplication before writing to MongoDB.
	4.	MongoDB Database – Stores clean data under logisticsDB → truck_data collection.
	5.	Dockerized Consumers – Run inside Docker containers with Dockerfile and docker-compose.
	6.	Consumer Group Scaling – Supports multiple consumer instances (e.g., 5 parallel consumers).
	7.	Confluent Sink Connector – Connects Kafka with MongoDB for ingestion.

**This repository is an excellent showcase of:** 

	•	Kafka → MongoDB streaming pipelines
	•	Data deduplication using unique IDs
	•	Schema management with Confluent Schema Registry
	•	Scalable consumer groups running in Docker
	•	End-to-end logistics data ingestion workflows

⸻

# **Features**

	•	CSV → Kafka → MongoDB streaming flow
	•	Schema Registry for schema enforcement
	•	Data cleansing & filtering in consumer code
	•	No duplicate IDs in MongoDB collection
	•	Dockerized consumers for easy deployment
	•	Scalable consumer group (run multiple instances dynamically)
	•	Confluent Sink Connector for seamless Kafka–MongoDB integration

⸻

# **Tech Stack**

	•	Confluent Kafka – Distributed event streaming platform
	•	Confluent Schema Registry – Enforces schema consistency
	•	MongoDB – NoSQL database for logistics data storage
	•	Python – Producer & consumer implementation
	•	Docker & Docker Compose – Containerized consumer deployment
	•	Confluent Kafka UI – For sink connector and monitoring

⸻

# **Project Workflow**

**Objective** - Build a real-time logistics data pipeline that ingests trip & truck data from CSV into MongoDB, ensuring cleansing, deduplication, and scalability.

**Workflow Steps**

	1.	Producer – Publishes logistics data (delivery_trip_truck_data.csv) into Kafka.
	2.	Schema Registry & Cluster – Enforces schema validation and handles scaling.
	3.	Consumer Group (via Docker) – Multiple consumer instances run in parallel to consume, filter, and cleanse data.
	4.	Deduplication – Consumer logic ensures no duplicate truck IDs are inserted into MongoDB.
	5.	MongoDB Storage – Cleaned data is stored inside logisticsDB → truck_data.
	6.	Confluent Sink Connector – Connects Kafka topic to MongoDB for automated ingestion.

⸻

📂 Repository Structure

```
kafka-to-mongodb-stream/
├── datasets/                   # Source dataset (delivery_trip_truck_data.csv)
│
├── Producer-Cosumer/
|	├── produce.py          #Producer code (CSV Data - Kafka Topic)
│   └── Consumer-Group
|       ├── consumer.py        #Consumer code (Kafka -> MongoDB With Cleansing and Filteration)
│   	└── docker file
|		└── docker-compose.yml
│
├── README.md               # Project documentation
├── LICENSE                 # License information
```

# **Key Learning Outcomes**

	•	How to build a real-time data pipeline with Kafka & MongoDB
	•	Using Schema Registry to enforce data quality
	•	Implementing cleansing & deduplication at the consumer level
	•	Running scalable consumers in Docker containers
	•	Using Confluent Sink Connector for database integration

⸻

# **🛡️ License**

This project is licensed under the MIT License.

⸻

# **🌟 About Me**

Hi there! I’m Krrish Sethiya. I’m a 3rd Year Grad at Medicaps University, Indore, currently specializing in Data Engineering.
