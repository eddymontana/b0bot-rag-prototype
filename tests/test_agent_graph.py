import os
import sys
import logging
from services.AgentService import app_graph

# Ensure the logger matches C2SI's verbose debugging standard
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_agent_test():
    print("\n" + "="*60)
    print("🚀 C2SI B0BOT: AGENTIC GRAPH INTEGRATION TEST")
    print("="*60)
    
    # ALIGNMENT: State must contain these keys for the Graph to validate
    inputs = {
        "query": "Recent ransomware and malware activity",
        "plan": [],
        "raw_results": [],
        "final_report": "",
        "next_step": ""
    }

    # ALIGNMENT: Use 'updates' mode to verify node transitions
    try:
        for output in app_graph.stream(inputs, stream_mode="updates"):
            for node_name, state_update in output.items():
                print(f"\n[NODE EXECUTION]: {node_name}")
                
                # Check for Vector DB Results (Retrieval Node)
                if "raw_results" in state_update:
                    results = state_update["raw_results"]
                    print(f"📊 Items Retrieved: {len(results)}")
                    
                    if len(results) > 0:
                        # ALIGNMENT: Switched 'title' to 'headlines' to match Extractor.py
                        first_headline = results[0].get("headlines")
                        source_url = results[0].get("newsURL")
                        print(f"✅ DATA VERIFIED: {first_headline}")
                        print(f"🔗 SOURCE: {source_url}")
                
                # Check for the LLM Final Summary (Generation Node)
                if "final_report" in state_update:
                    report = state_update["final_report"]
                    print("\n📜 FINAL INTELLIGENCE REPORT (MISTRAL):")
                    print("-" * 50)
                    if report:
                        print(report)
                    else:
                        print("⚠️ WARNING: Generator node returned empty state.")
                    print("-" * 50)

    except Exception as e:
        logger.error(f"Graph failed at runtime: {e}")
        print(f"❌ TEST FAILED: {str(e)}")

if __name__ == "__main__":
    run_agent_test()