# b0bot-rag-prototype
## GSoC 2026 Prototype for C2SI

# Goal
This prototype validates the migration of b0bot from a linear retrieval tool to an Agentic RAG system. It focuses on modularizing the news ingestion pipeline and establishing a CI/CD-ready environment.


# Implementation Details (Phase 1)
## 1. Verification & Testing
Mocked Unit Tests: Uses unittest.mock to verify the CyberNews scraper and extractor logic without hitting live endpoints.

CI/CD Pipeline: GitHub Actions automated to run tests on every push, ensuring dependency stability.

## 2. Infrastructure & Deployment
Optimized Dockerfile: Multi-stage build using a Python-slim base. Includes Playwright dependencies and a non-root user (appuser) for security compliance.

Orchestration: docker-compose.yml configured for environment parity across local and remote dev.

## 3. Architecture
Service-Based Design: Refactored CyberNews.py as a standalone module to fit into the b0bot service layer.

JSend Standard: Flask API responses follow JSend specifications for predictable frontend consumption.


## Stack
Core: Python 3.12, Flask, Docker
Intelligence: LangGraph, LangChain (Mistral-7B via API)
Memory: Pinecone (Vector Index), HuggingFace (Embeddings)
Scraping: Playwright

## Setup
## 1. Environment Variables
Create a .env file in the root:

PINECONE_API_KEY=your_key
HUGGINGFACEHUB_API_TOKEN=your_token
MISTRAL_API_KEY=your_key

## 2. Deployment
git clone https://github.com/eddymontana/b0bot-rag-prototype.git
cd b0bot-rag-prototype
docker-compose up --build
