# ASTERRA DevOps Technical Assignment 🌍🚀

## Overview
This repository contains the complete implementation of the ASTERRA DevOps technical challenge. The project demonstrates a fully automated, cloud-native GIS data pipeline on AWS, managed via Infrastructure as Code (IaC) and CI/CD.

The system ingests GeoJSON files via S3, validates them using a containerized Python service, and stores the spatial data in a PostgreSQL/PostGIS database.

## 🏗 System Architecture
The infrastructure is designed with a focus on security and network isolation:
* **Networking:** A custom VPC with Public and Private subnets across multiple Availability Zones.
* **Data Layer:** AWS RDS Instance (PostgreSQL + PostGIS extension) and an S3 Ingestion Bucket.
* **Processing:** A containerized Python microservice (deployed on ECS or EC2) that triggers on S3 events.
* **Public Layer:** A publicly accessible service (e.g., WordPress/OSM) served on an Elastic IP.
* **Observability:** All application logs and processing results are exported to Amazon CloudWatch.



---

## 🛠 Tech Stack
* **Cloud:** AWS (RDS, S3, ECR, CloudWatch, IAM)
* **IaC:** Terraform
* **Containers:** Docker (Base image: Python with GeoPandas)
* **CI/CD:** GitHub Actions
* **GIS Tools:** PostGIS, GeoPandas, GDAL

---

## 🚀 Getting Started

### Prerequisites
* AWS CLI configured with appropriate credentials.
* Terraform installed (`v1.0.0+`).
* Docker installed locally for image building.

### One-Click Deployment
The entire environment is reproducible. To deploy the infrastructure and the application, run:
```bash
chmod +x deploy.sh
./deploy.sh --region us-east-1
Note: This script initializes Terraform, builds the Docker image, pushes it to ECR, and applies the plan.

📁 Repository Structure
Plaintext

├── .github/workflows/    # CI/CD Pipeline (Build, Test, Version, Deploy)
├── terraform/            # IaC scripts
│   ├── modules/          # VPC, RDS, S3, IAM modules
│   ├── main.tf           # Main entry point
│   ├── variables.tf      # Configurable parameters
│   └── outputs.tf        # Key resource identifiers
├── app/                  # Data Processing Microservice
│   ├── src/              # Logic for S3 trigger & RDS upload
│   ├── Dockerfile        # Custom image with GeoPandas installation
│   └── requirements.txt
├── scripts/              # Setup and cleanup automation
└── docs/                 # Design diagrams and "Half-pager" summary
🔐 Security & Maintainability
Principle of Least Privilege: IAM policies are strictly scoped to specific S3 buckets and RDS resources.

Network Hardening: Security Groups restrict traffic. The DB is only accessible from within the VPC.

Secrets Management: DB credentials and sensitive keys are managed via environment variables (no hardcoded secrets).

Remote State: Terraform state is stored in a dedicated private S3 bucket to ensure consistency.

🧪 Testing the Pipeline
Validation: terraform validate ensures infrastructure integrity.

Integration Test: * Upload a sample.geojson to the ingestion S3 bucket.

Check CloudWatch Logs to see the "Validation Successful" and "Data Loaded" messages.

Query the RDS table to verify the spatial record exists.

📝 Work Summary (The "Half-Pager")
My detailed work summary, including architectural decisions, challenges with PostGIS automation, and technical trade-offs, is hosted in this public S3 bucket: 👉 []

Contact: [Ahmad Wattad] | [ahmadwattadgr@gmail.com]
