import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from services.AgentState import AgentState

load_dotenv()

def summarizer_node(state: AgentState):
    """
    The Reporter: Transforms raw vectors/headlines into a C2SI-standard 
    intelligence briefing using Mistral AI.
    """
    raw_data = state.get("raw_results", [])
    
    # 1. Graceful Degradation: If no news was found, let the user know why.
    if not raw_data:
        return {
            "final_report": "The b0bot agent scanned the sources but found no critical threats matching your query at this time.",
            "next_step": "end"
        }

    # 2. Initialize Mistral (Using a more robust model for analysis)
    llm = ChatMistralAI(
        model="mistral-small-latest", 
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2 # Slightly higher for better synthesis of news
    )
    
    # 3. Format headlines for the prompt
    headlines_text = "\n".join([f"- {item.get('title', 'N/A')}" for item in raw_data[:15]])

    # 4. C2SI Professional Persona Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Senior Cyber Security Threat Intelligence Analyst at C2SI. "
                   "Your goal is to provide concise, actionable intelligence briefings."),
        ("user", "Summarize these raw security headlines into a 3-point 'Executive Summary'. "
                 "Focus on impact and urgency.\n\nHEADLINES:\n{headlines}")
    ])

    try:
        print("--- SUMMARIZER: Generating Final Intelligence Report ---")
        chain = prompt | llm
        response = chain.invoke({"headlines": headlines_text})
        
        # C2SI Standard: We return the content and CLEAR the next_step 
        # so the graph knows we are done.
        return {
            "final_report": response.content,
            "next_step": "complete" 
        }
        
    except Exception as e:
        print(f"--- SUMMARIZER CRITICAL ERROR: {e} ---")
        return {
            "final_report": f"Intelligence synthesis failed: {str(e)}",
            "next_step": "error"
        }