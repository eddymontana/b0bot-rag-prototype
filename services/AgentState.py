from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # The original user input
    query: str
    
    # The steps the agent decided to take
    plan: List[str]
    
    # Annotated with operator.add allows nodes to APPEND to the list 
    # rather than overwriting it (C2SI standard for multi-source scraping)
    raw_results: Annotated[List[dict], operator.add]
    
    # The final output for the UI
    final_report: str
    
    # Logic control
    next_step: str
    
    # --- C2SI SAFETY ADDS ---
    
    # Tracks loop count to prevent infinite API calls
    iteration_count: int 
    
    # Stores technical errors for the /analyze error response
    errors: List[str]