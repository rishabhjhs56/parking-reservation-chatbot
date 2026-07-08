# 🚗 SmartPark AI – RAG Powered Parking Reservation Chatbot

## Overview
SmartPark AI is a LangChain-based RAG chatbot for parking reservations with Human-in-the-Loop approval.

### Stage 1
- RAG using Azure OpenAI + Milvus
- Reservation conversation
- Guardrails

### Stage 2
- SQLite reservation persistence
- Admin Agent
- Human approval
- Flask Approval API
- Email notifications
- Logging
- RAG Evaluation
- Pytest
- GitHub Actions CI

## Architecture
`docs/architecture/stage2_architecture.png`


## ⚙️ Tech Stack

| Technology      | Purpose                           |
|-----------------|-----------------------------------|
| Python          | Backend Development               |
| LangChain       | RAG Orchestration                 |
| Azure OpenAI    | LLM + Embeddings                  |
| Milvus          | Vector Database                   |
| SQLite          | Reservation Database              |
| Flask           | Admin Approval API                |
| Gmail SMTP      | Email Notifications               |
| Docker          | Milvus Deployment                 |
| Pytest          | Unit Testing                      |
| GitHub Actions  | CI/CD Automation                  |


## 🚀 Features

### 🧠 RAG-based Question Answering

Provides accurate, context-aware answers using Azure OpenAI and Milvus.

- Parking charges & policies
- Locations & facilities
- Payment methods
- EV & overnight parking
- Working hours & contact details

---

### 🤖 Reservation Agent (Finite State Machine)

Guides users through a conversational booking workflow.

- Collects customer & vehicle details
- Validates user inputs
- Stores reservation in SQLite
- Escalates request for admin approval

---

### 🗄️ SQLite Database

Stores reservation and parking slot information.

- Customer records
- Reservation details
- Slot availability
- Booking status

---

### 👨‍💼 Human-in-the-Loop Approval

Ensures every reservation is reviewed by an administrator.
`docs/architecture/human_in_loop_flow.png`

- Pending approval
- Approve / Reject
- Automatic status updates

---

### 📧 Email Notifications

Sends reservation requests directly to the administrator.

- Reservation summary
- Masked sensitive information
- One-click approval links

---

### 🌐 Flask Admin API

Provides REST endpoints for reservation management.

- Approve reservation
- Reject reservation
- Revert to Pending

---

### 📋 Logging & Monitoring

Captures key application events.

- Reservations
- Emails
- Admin actions
- Errors

---

### 🔒 Guardrails

Protects the chatbot from unsafe interactions.

- Input validation
- Sensitive data masking
- Abuse prevention

---

### 🧪 Automated Testing

Unit tests implemented using **Pytest**.

- Reservation Agent
- Admin Agent
- Chat Orchestrator
- SQLite Client
- Guardrails
- Email Service

---

### 📊 RAG Evaluation

Measures retrieval performance.

- Accuracy
- Precision@K
- Recall@K
- Response Time

---

### ⚙️ Continuous Integration (CI/CD)

Automates project validation using GitHub Actions.

- Dependency installation
- Automated testing
- Build validation


## ⚙️ Installation & Setup

```bash
git clone <repo>
cd parking-reservation-chatbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:

```env
AZURE_API_KEY=
AZURE_ENDPOINT=
AZURE_API_VERSION=2024-02-01
AZURE_DEPLOYMENT_NAME=
AZURE_EMBEDDING_DEPLOYMENT=
MILVUS_URI=http://localhost:19530
MILVUS_COLLECTION_NAME=parking_information
EMAIL_ADDRESS=
EMAIL_PASSWORD=
ADMIN_EMAIL=
```

### Start Milvus

```bash
cd docker/milvus
docker-compose up -d
```

### Initialize Database

```bash
python -m app.database.init_db
python -m app.database.seed_slots
```

### Index Documents

```bash
python -m app.rag.index_documents
```

### Start Flask API

```bash
python -m app.api.admin_api
```

### Run Chatbot

```bash
python main.py
```

### Admin Console

```bash
python -m misc_scripts.admin_console
```

### Run Tests

```bash
python -m pytest -v
```

### Run RAG Evaluation

```bash
python -m app.evaluation.rag_evaluation
```

Evaluation report is saved in:

`docs/evaluation_reports/rag_evaluation_report.txt`


## 🚀 Future Enhancements
### Stage 3
- MCP Server Integration
- FastAPI-based MCP Server
- Secure Reservation Processing
- Reservation File Storage

### Stage 4
- LangGraph Orchestration
- End-to-End Workflow Automation
- Integration Testing
- Load & Performance Testing


## Author

**Rishabh Gupta**
