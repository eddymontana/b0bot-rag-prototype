import os
import pytest
from dotenv import load_dotenv

# Load env for local testing
load_dotenv()

def test_agentic_stack_imports():
    """C2SI Standard: Verify 2026 Agentic Framework dependencies (Mistral Stack)."""
    try:
        # Core Agentic Stack
        import langgraph
        import langchain_pinecone
        from langchain_mistralai import ChatMistralAI  # Corrected from OpenAI
        
        # ML Stack (Specifically for all-MiniLM-L6-v2 model)
        import sentence_transformers
        from pinecone import Pinecone
        
        print("\n✅ AI/ML Stack verified (LangGraph, Pinecone, SentenceTransformers, Mistral).")
    except ImportError as e:
        pytest.fail(f"❌ Dependency Missing: {e}. Check requirements.txt")

def test_flask_app_context():
    """Ensure the Flask entry point (app.py) is bootable."""
    try:
        # Import the app factory or instance
        from app import create_app
        app = create_app()
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            # Check the health endpoint we built in app.py
            response = client.get('/health')
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == "healthy"
            print("✅ Flask Server Context: Bootable and Healthy.")
    except Exception as e:
        pytest.fail(f"❌ Flask Boot Failure: {e}")

def test_config_readiness():
    """Custom C2SI Check: Verify the News Scraper config is accessible."""
    config_path = 'cybernews/news_types.json'
    # Use os.path to check existence
    assert os.path.exists(config_path), f"❌ Critical Config Missing: {config_path}"
    print(f"✅ Config Found: {config_path}")