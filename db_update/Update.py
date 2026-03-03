import sys
import os
import uuid
from dotenv import dotenv_values
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Path alignment for internal modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybernews.CyberNews import CyberNews

# Load Environment
config = dotenv_values(".env")
PINECONE_API = config.get("PINECONE_API_KEY")

# Configure Pinecone
pc = Pinecone(api_key=PINECONE_API)
index_name = "cybernews-index"
namespace = "c2si"

# 1. Index Management (Optimized: Check before deleting)
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=384, 
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

index = pc.Index(index_name)

# Load Embedding Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Fetch News
news_scraper = CyberNews()
categories = ["general", "cyberAttack", "vulnerability", "malware", "security", "dataBreach"]

# 2. Batch Processing Engine (The AI/ML standard)
batch_limit = 100
upsert_batch = []

print(f"🚀 Starting news update for index: {index_name}...")

for category in categories:
    articles = news_scraper.get_news(category)
    print(f"--- Fetching {len(articles)} articles for category: {category} ---")
    
    for article in articles:
        # Prepare content for embedding
        content_to_embed = f"{article['headlines']} {article['fullNews']}"
        
        # Create Vector
        vector = model.encode(content_to_embed).tolist()
        
        # Metadata Alignment (Added 'category' and 'timestamp' for better filtering)
        # Note: We use the ID from our Sorting class (which is now a deterministic hash)
        doc_id = str(article["id"])
        
        metadata = {
            "headlines": article["headlines"],
            "author": article["author"],
            "fullNews": article["fullNews"][:1000],  # Pinecone metadata size limit precaution
            "newsURL": article["newsURL"],
            "newsImgURL": article["newsImgURL"],
            "newsDate": article["newsDate"],
            "category": category  # Crucial for filtered RAG queries
        }
        
        upsert_batch.append((doc_id, vector, metadata))
        
        # 3. Perform Batch Upsert
        if len(upsert_batch) >= batch_limit:
            index.upsert(vectors=upsert_batch, namespace=namespace)
            print(f"✅ Upserted batch of {len(upsert_batch)} articles.")
            upsert_batch = []

# Final sweep for remaining articles
if upsert_batch:
    index.upsert(vectors=upsert_batch, namespace=namespace)
    print(f"✅ Final batch of {len(upsert_batch)} upserted.")

print("✨ Database update complete.")