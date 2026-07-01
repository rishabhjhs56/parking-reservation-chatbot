# 🚗 SmartPark AI - RAG Parking Chatbot System

## 📌 Overview
SmartPark AI is an AI-powered Parking Chatbot built using Retrieval-Augmented Generation (RAG).  
It helps users get parking-related information (charges, locations, rules, etc.) and also supports a basic reservation flow.

The system uses:
- LangChain for orchestration
- Azure OpenAI embeddings for vector representation
- Milvus vector database for semantic search

---

# 🏗️ System Architecture

User → Chatbot → Intent Detection →  
→ RAG Retriever (Milvus) OR Reservation Agent → LLM Response

---

# ⚙️ Tech Stack

- Python
- LangChain
- Azure OpenAI (Embeddings)
- Milvus Vector Database
- Docker

---

# 🧠 How the System Works (RAG Pipeline)

## Step 1: Document Loading
Parking-related documents (rules, charges, locations, FAQs) are loaded from local files.

## Step 2: Text Splitting
Documents are split into small chunks to improve retrieval accuracy.

## Step 3: Embedding Generation
Each chunk is converted into vector embeddings using Azure OpenAI embedding model.

## Step 4: Vector Storage (Milvus)
Embeddings are stored inside Milvus collection for fast semantic search.

## Step 5: Retrieval + Response Generation
- User query is converted into embedding
- Similar chunks are retrieved from Milvus
- LLM generates final answer using retrieved context

---

# 💬 Features

## 1. RAG-based Q&A
Users can ask:
- Parking charges
- Locations (e.g., Jhansi)
- Rules and policies
- Payment methods
- Facilities

## 2. Reservation System
Conversational booking flow that collects:
- First Name
- Last Name
- Vehicle Number
- Vehicle Type
- Date
- Start Time
- End Time

## 3. Vector Search
- Semantic search using Milvus
- Context-aware responses

---

# 🛠️ Installation & Setup

## Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd parking-reservation-chatbot

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt

##Step 3: Start Milvus (Docker Required)

docker-compose up -d

## Step 4: Index Documents

python -m app.rag.index_documents

## Step 5: Run Chatbot

python main.py


## Step 6: Stop Services (Optional)
docker-compose down
