# Custom RAG Deployment with AWS Services

## Project Overview

This project showcases the deployment of a full-stack application, including frontend, backend, and database, using AWS cloud infrastructure. The primary goal is to ensure high security, availability, and performance while gaining hands-on experience in deploying projects on AWS.

I used various AWS services, including S3 for object storage, RDS for database management, EC2 for compute resources, and VPC for private networking. Key components such as IAM, API Gateway, Application Load Balancer, and security groups were used to establish a robust and secure environment. This deployment integrates industry best practices to achieve scalability, reliability, and fault tolerance.

**AWS Services**:  
 ![S3](https://img.shields.io/badge/AWS-S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white)
![RDS](https://img.shields.io/badge/AWS-RDS-527FFF?style=for-the-badge&logo=amazon-rds&logoColor=white)
![EC2](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![VPC](https://img.shields.io/badge/AWS-VPC-232F3E?style=for-the-badge&logo=amazon-vpc&logoColor=white)
![API Gateway](https://img.shields.io/badge/AWS-API_Gateway-FF4F00?style=for-the-badge&logo=amazon-api-gateway&logoColor=white)
![IAM](https://img.shields.io/badge/AWS-IAM-FF9900?style=for-the-badge&logo=amazon-iam&logoColor=white)
![Application Load Balancer](https://img.shields.io/badge/AWS-ALB-009688?style=for-the-badge&logo=amazon-elastic-load-balancer&logoColor=white)
![Eraser.io](https://img.shields.io/badge/Eraser.io-00A8E8?style=for-the-badge&logo=eraser&logoColor=white)

## AWS Architecture

![Alt Text](Architecture)

### Key Components:

- **Frontend & Backend**:

  - Developed using React to provide a responsive and user-friendly interface.
  - Built backend with python to handle API requests and communicate with the database.

- **AWS Services**:
  - **VPC**: Firstly, I designed network with 1 public subnet for frontend, 2 private subnet for backend, and 2 private subnet with 2 difference availability zones for database for High Availability.
  - **S3**: Used S3 bucked to store semi structured data files.
  - **IAM**: Created **read-only** access policy for security, so the only specific EC2 backend instance be able to read data files.
  - **RDS**: PostgreSQL database used to store structures format of data.
  - **EC2**: Used one EC2 instance for frontend, and 2 EC2 instances for backend.
  - **APIGateaway**: Configured to ensure backend is only accessible internally, not via browser or internet.
  - **ALB**: used Application LoadBalancer to distribute the backend request across 2 EC2 instances.

---

## Deployment Architecture

### 1. Custom VPC

Firstly, I created Custom VPC to create an isolated environment.

- **Public Subnet**:
  - Host the EC2 instance for the frontend.
  - Internet Gateway is attached to public subnet to enable internet access and make it public.
- **Private Subnets**:
  - Host the RDS instance and 2 EC2 instances for the backend and database.
  - Configured NAT Gateway to allow communication from the private subnet to the internet for necessary updates.

![Alt Text](SUBNET)

### 2. EC2 instances

- **Public EC2 Instance:**
  I created one EC2 instance to host my frontend. I enabled a public IP for the instance, installed Docker on it, and used Docker Compose to bring up the project.

- **Private EC2 Instances:**
  I created two EC2 instances to host my backend. During the development stage, I temporarily enabled public IPs to make them accessible for cloning the project. After cloning, I installed Docker on them, used Docker Compose to bring up the project, and reverted the instances to private for security.

![Alt Text](instances)

### 3. IAM Policy

I created a role with the AmazonS3ReadOnlyAccess policy attached to it and assigned this role to my two backend instances. Additionally, I configured a bucket policy on my S3 bucket to allow access only to principals with a specific ARN.

### 4. Security Rules

**For Public Instance**

- **Inbound Rules**:
  - Port `3000` accessible via the internet for the frontend.
  - Port `22` accessible via the internet for the ssh.
  - Protocol ICMP accessible via the internet for the ping the instance.
- **Outbound Rules**:
  - All ports and protocol is allowed from the frontend instance.

**For Private Instance**

- **Inbound Rules**:
  - Port `8000` is open to only those services that has security group "sg-0c42666672cbb1ea1 / scalableproject-vpclink-sg" attached with it, in our case it is ALB.
- **Outbound Rules**:
  - All ports and protocol is allowed from the backend instances.

**For RDS Instance**

- **Inbound Rules**:
  - Port `5432` is open for only 10.0.2.0/24, 10.0.3.0/24 ranges, which are internal CIDR range of our backend instances.
- **Outbound Rules**:
  - All ports and protocol is allowed from the backend instances.

**For VPC Link**

- **Inbound Rules**:
  - No Inbound rules, as it is use internally to send request from API Gateaway to ALB.
- **Outbound Rules**:
  - Port `80` and `443` is open to only those services that has security group "sg-0c42666672cbb1ea1 / scalableproject-vpclink-sg" attached with it, in our case it is ALB.

![Alt Text](SG)

**For ALB**

- **Inbound Rules**:
  - Port `80` and `443` is open to only those services that has security group "sg-0e4fb68719bfbec57 / test-scalableproject-vpc-link-sg" attached with it, in our case it is vpc link.
- **Outbound Rules**:
  - Port `8000` is open for only 10.0.2.0/24, 10.0.3.0/24 ranges, which are internal IPs of backend instances.

### 5. Application Load Balancer

- **Target Group:**
  I created a Target Group and registered the backend EC2 instances as targets. This ensures that the ALB can route traffic to the appropriate instances.

- **Load Balancer:**
  I set up an Application Load Balancer (ALB) and linked it to the Target Group. The ALB is configured to distribute incoming traffic evenly across the backend instances, ensuring high availability and fault tolerance.

![Alt Text](TragetGroup)
![Alt Text](ALB)

### 6. API GateAway

First, I created a VPC link to enable API Gateway to communicate with the ALB internally. After that, I created the API and, at the integration level, connected it to the ALB.

---
