import os
from playwright.sync_api import sync_playwright
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize Pinecone & Embeddings
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "b0bot-index" # Ensure you created this index in Pinecone console (1536 or 384 dim)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@tool
def fetch_cyber_news(category: str):
    """
    C2SI Standard: Playwright Scraper + Pinecone Vector Memory.
    Bypasses anti-bot measures and stores intelligence for RAG.
    """
    url_map = {
        "malware": "https://www.infosecurity-magazine.com/malware/",
        "cyberAttack": "https://cyware.com/search?search=cyber%20attack",
        "Ransomware": "https://www.bleepingcomputer.com/tag/malware/"
    }
    
    url = url_map.get(category, url_map["malware"])
    results = []
    
    # --- PHASE 1: PLAYWRIGHT SCRAPING ---
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()
        
        try:
            print(f"--- SCRAPER: Accessing {url} ---")
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_selector("body", timeout=5000)
            
            selector = "h3, h4, .cy-card__title"
            page.wait_for_selector(selector, state="attached", timeout=10000)
            
            items = page.query_selector_all(selector)
            for item in items[:10]:
                text_content = item.inner_text().strip()
                if len(text_content) > 20:
                    results.append({"title": text_content, "source": url})
            
        except Exception as e:
            print(f"--- SCRAPER ERROR: {str(e)} ---")
        finally:
            browser.close()

    # --- PHASE 2: PINECONE VECTOR STORAGE (The 'Best Results' Add) ---
    if results:
        index = pc.Index(index_name)
        for i, item in enumerate(results):
            # Create a unique ID and embed the title
            vector = embeddings.embed_query(item['title'])
            index.upsert(vectors=[(
                f"{category}-{i}", 
                vector, 
                {"title": item['title'], "source": item['source'], "category": category}
            )])
        print(f"--- RAG: Successfully vectorized {len(results)} items to Pinecone ---")

    return results