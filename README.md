# b0bot-rag-prototype 🤖🛡️

### **Autonomous Agentic Cyber-Threat Intelligence**
*A GSoC 2026 Proposal Prototype for C2SI (Community-owned Cloud Services Initiative)*

---

## 🚀 Overview
This repository serves as the technical foundation for my GSoC 2026 proposal. It evolves the 2024 **b0bot** framework from a linear retrieval tool into an **Autonomous Agentic RAG (Retrieval-Augmented Generation)** system. 

Key improvements include **deterministic unit testing**, **multi-stage containerization**, and a **modular LangGraph architecture** designed for scalable threat analysis.

---

## ✨ Key Features (Phase 1 Complete)

### 1. Production-Grade Reliability
* **Deterministic Mocking:** Implemented a robust `unittest` suite using `unittest.mock` to verify scraping and extraction logic without network dependency.
* **CI/CD Readiness:** The testing suite is integrated directly into the build pipeline to ensure only verified code is deployable.

### 2. Modern Containerization
* **Multi-Stage Docker Build:** Optimized Dockerfile using `playwright/python` base to ensure a lightweight production image with all necessary browser dependencies.
* **Orchestration:** Pre-configured `docker-compose.yml` for seamless environment parity across development and production.

### 3. Agentic Foundation
* **Modular Service Design:** Refactored the `CyberNews` service to act as a standalone tool for a future LangGraph-driven autonomous loop.
* **JSend-Compliant API:** Standardized Flask response structures for both threat analysis and news retrieval.

---

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **Framework:** Flask (Application Factory Pattern)
* **AI/ML:** LangGraph, LangChain, SentenceTransformers
* **Vector DB:** Pinecone
* **Automation:** Playwright (Web Scraping)
* **Infrastructure:** Docker, Docker Compose

---

## 🚦 Quick Start

### **Prerequisites**
- Docker & Docker Compose installed.
- # .env template
PINECONE_API_KEY=your_pinecone_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
MISTRAL_API_KEY=your_mistral_key_here

### **Installation & Deployment**
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/eddymontana/b0bot-rag-prototype.git](https://github.com/eddymontana/b0bot-rag-prototype.git)
   cd b0bot-rag-prototype