import pytest
import os
import logging
from dotenv import load_dotenv

# Load env for local testing
load_dotenv()

def test_agentic_stack_imports():
    """C2SI Standard: Verify 2026 Agentic Framework dependencies."""
    try:
        # Core Agentic Stack
        import langgraph
        import langchain_pinecone
        from langchain_openai import ChatOpenAI
        
        # ML Stack (Specifically for your all-MiniLM-L6-v2 model)
        import sentence_transformers
        from pinecone import Pinecone
        
        print("\n✅ AI/ML Stack verified (LangGraph, Pinecone, SentenceTransformers).")
    except ImportError as e:
        pytest.fail(f"❌ Dependency Missing: {e}. Run 'pip install -r requirements.txt'")

def test_flask_app_context():
    """Ensure the Flask entry point (app.py) is bootable."""
    try:
        from app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            # We check the root or a heartbeat/health endpoint
            response = client.get('/')
            assert response.status_code in [200, 302, 404] # 404 is okay if root isn't defined yet
            print("✅ Flask Server Context: Bootable.")
    except Exception as e:
        pytest.fail(f"❌ Flask Boot Failure: {e}")

def test_config_readiness():
    """Custom C2SI Check: Verify the News Scraper config is accessible."""
    config_path = 'cybernews/news_types.json'
    assert os.path.exists(config_path), f"❌ Critical Config Missing: {config_path}"
    print(f"✅ Config Found: {config_path}")