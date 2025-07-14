# COMP3480 Lab 8 - Multi-Service System with Docker Compose

## Overview

Lab 8 extends Lab 7 by implementing a comprehensive multi-service system using Docker Compose. This lab demonstrates the integration of various services including shared file storage, caching, email, API services, and database operations.

## New Services Added

### 1. MinIO Object Storage (Shared File System)
- **Purpose**: Provides S3-compatible object storage for file sharing
- **Port**: 9000 (API), 9001 (Console)
- **Access**: Web UI at http://localhost:9001 (minioadmin/minioadmin123)
- **Use Case**: Store and retrieve files across services

### 2. Redis Cache (Shared Memory)
- **Purpose**: In-memory data structure store for caching and shared memory
- **Port**: 6379
- **Use Case**: Store session data, cache frequently accessed data, inter-service communication

### 3. Postfix Email Server (SMTP)
- **Purpose**: Email sending capability for the system
- **Port**: 1587 (SMTP)
- **Use Case**: Send notifications, alerts, and system emails
- **Note**: Configured for real email sending (will likely be rejected by spam filters)

## Architecture

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   FastAPI       │   │     MySQL       │   │     Redis       │
│   Server        │   │   Database      │   │     Cache       │
│   :8080         │   │    :3307        │   │    :6379        │
└─────────────────┘   └─────────────────┘   └─────────────────┘
                                          
┌─────────────────┐   ┌─────────────────┐
│     MinIO       │   │    Postfix      │
│ Object Storage  │   │ Email Server    │
│ :9000/:9001     │   │     :1587       │
└─────────────────┘   └─────────────────┘
```

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ with pip

### 1. Start All Services

```bash
cd "Lab 8"
docker-compose up -d
```

This will start all services:
- MySQL Database (port 3307)
- FastAPI Server (port 8080) 
- Redis Cache (port 6379)
- MinIO Object Storage (ports 9000, 9001)
- Postfix Email Server (port 1587)

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Services Are Running

```bash
docker-compose ps
```

All services should show as "Up" status.

## Using the CLI Driver

The enhanced CLI driver provides access to all services through a clean, organized menu:

```bash
python cli_driver.py
```

### Menu Structure

**Main Menu:**
- **1. FastAPI Services Menu** - Access all Lab 7 API routes
- **2. Redis Cache Service** - Test shared memory operations
- **3. MinIO File Service** - Test object storage operations  
- **4. Postfix Email Service** - Test email sending capabilities
- **5. View Postfix Logs** - Show email delivery status and spam filter behavior
- **6. Database Operations** - Execute database queries
- **7. Run All Tests** - Automated testing of all services
- **8. Check All Services Status** - Health check for all services

### Service Demonstrations

#### Redis Cache Service
- Store and retrieve key-value pairs
- Test TTL (time-to-live) functionality
- List all stored keys
- Demonstrate shared memory capabilities

#### MinIO File Storage
- Create buckets for file organization
- Upload text files to object storage
- Download and verify file contents
- List files in buckets

#### Postfix Email Service
- Test SMTP connection
- Create properly formatted email messages
- Send REAL emails to jaldua@wit.edu (configurable)
- Demonstrate spam filter behavior (expected rejection)
- Show real-time delivery logs and analysis
- Handle connection errors gracefully

## Running Tests

### Automated Testing

Run all tests including the new services:

```bash
python test.py
```

This will execute:
- **FastAPI Tests**: All Lab 7 API endpoints
- **Database Tests**: SQL query operations
- **Redis Tests**: Cache connection and operations
- **MinIO Tests**: Object storage operations
- **Postfix Tests**: Email functionality and structure

### Individual Service Testing

Use the CLI driver menu options to test individual services interactively.

## Service Configuration

### MinIO Configuration
- **Username**: minioadmin
- **Password**: minioadmin123
- **API Endpoint**: http://localhost:9000
- **Console**: http://localhost:9001

### Redis Configuration
- **Host**: localhost
- **Port**: 6379
- **No authentication required

### Postfix Configuration
- **SMTP Host**: localhost
- **SMTP Port**: 1587
- **Allowed Domains**: wit.edu
- **Email Behavior**: Real sending (no relay host configured)
- **Expected Result**: Rejection by recipient servers due to spam filters

### Database Configuration
- **Host**: localhost
- **Port**: 3307
- **Username**: root
- **Password**: secret_password

## Docker Compose Services

```yaml
services:
  mysql:      # Database service
  fastapi:    # API service  
  redis:      # Cache service
  minio:      # Object storage
  postfix:    # Email service
```

All services are configured with:
- Persistent volumes for data
- Proper networking between containers
- Health checks and restart policies

## Use Cases Demonstrated

1. **File Sharing**: Upload files via MinIO, access from any service
2. **Caching**: Store frequently accessed data in Redis
3. **Notifications**: Send email alerts via Postfix
4. **API Integration**: All services accessible through FastAPI
5. **Data Persistence**: Database and file storage persist across restarts

## Troubleshooting

### Common Issues

**Services not starting:**
```bash
docker-compose down
docker-compose up -d
```

**Port conflicts:**
- Check if ports 3307, 6379, 8080, 9000, 9001, 1587 are available
- Modify docker-compose.yaml port mappings if needed

**Connection timeouts:**
- Wait 30-60 seconds for all services to fully initialize
- Use "Check All Services Status" in CLI to verify

### Service URLs

- **FastAPI**: http://localhost:8080
- **MinIO Console**: http://localhost:9001
- **Redis**: localhost:6379
- **MySQL**: localhost:3307
- **SMTP**: localhost:1587

## Development Notes

- **Email sending**: Configured for real sending, will likely be rejected by spam filters (expected behavior)
- Services are configured for development, not production use
- All credentials are default/test values
- Persistent volumes maintain data between container restarts
- Postfix attempts real email delivery to demonstrate spam filter behavior

## Technologies Used

- **Python 3.8+** – Programming language for database integration
- **mysql-connector-python** – MySQL database connector for Python
- **FastAPI** – API framework for web service endpoints
- **Docker Compose** – Multi-container application orchestration
- **MySQL 9.3** – Relational database management system
- **unittest** – Automated testing framework
- **requests** – HTTP client for API testing 
- **redis** – In-memory data store for caching and session management
- **minio** – S3-compatible object storage for file sharing
- **postfix** – SMTP email server for sending and receiving emails