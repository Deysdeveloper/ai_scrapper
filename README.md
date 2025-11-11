# Scalable Web Scraping API

A production-ready web scraping solution with a RESTful API interface, containerized architecture, and cloud deployment capabilities.

## 🏗️ Architecture Overview

This project consists of three main components working together to provide a scalable web scraping service:

### 1. **Scraper Worker**
- **Technology Stack**: Python + Playwright
- **Execution Model**: Runs on a schedule or queue-based system
- **Containerization**: Deployed in a separate container for isolation
- **Responsibilities**:
  - Performs actual web scraping tasks
  - Handles browser automation via Playwright
  - Processes scraping jobs from the queue
  - Stores results in the database

### 2. **FastAPI Server**
- **Framework**: FastAPI (Python)
- **Architecture**: Simple REST API
- **Key Features**:
  - Trigger scraping jobs on-demand
  - Retrieve cached/stored scraping results
  - Provide API endpoints for client interaction
  - Handle request validation and response formatting

### 3. **Database Layer**
- **Options**: PostgreSQL or Redis
- **Purpose**: 
  - Temporary storage for job queues
  - Persistent storage for scraping results
  - Caching layer for frequently accessed data

## 🚀 Development Setup

### Prerequisites
- Docker
- Docker Compose

### Local Development
Use Docker Compose for easy local development setup:

```bash
docker-compose up
```

This will spin up all services locally:
- FastAPI server
- Scraper worker
- Database (PostgreSQL/Redis)

## 📦 Deployment

### Deployment Option
**Target**: Linode VPS

The application is designed to be deployed on a cloud VPS with all components containerized for easy management and scaling.

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI |
| Scraper | Python + Playwright |
| Database | PostgreSQL / Redis |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Deployment | Linode VPS |

## 📋 Project Structure

```
.
├── api/                    # FastAPI application
├── worker/                 # Scraper worker service
├── docker-compose.yml      # Local development setup
└── README.md              # Project documentation
```

## 🔄 Workflow

1. **API Request**: Client sends a scraping request to the FastAPI server
2. **Job Queue**: Server adds the job to the queue in the database
3. **Worker Processing**: Scraper worker picks up the job and executes it
4. **Result Storage**: Worker stores results in the database
5. **Result Retrieval**: Client can fetch results via API endpoints

## 📝 API Endpoints

- `POST /scrape` - Trigger a new scraping job
- `GET /results/{job_id}` - Retrieve scraping results
- `GET /status/{job_id}` - Check job status

## 🔐 Environment Variables

Configure the following environment variables:
- Database connection strings
- API keys (if needed)
- Scraping configuration
- Worker schedule settings

## 🤝 Contributing

Contributions are welcome! Please follow the standard fork-and-pull request workflow.

## 📄 License

[Add your license here]
