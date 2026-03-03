from services.AgentState import AgentState
from services.AgentTools import fetch_cyber_news

def executor_node(state: AgentState):
    """
    C2SI Executor: Iterates through the plan and fetches intelligence.
    Includes safety counters and stateless data handling.
    """
    plan = state.get("plan", [])
    current_results = []
    current_count = state.get("iteration_count", 0)
    
    # 1. Logic Check: If the plan is empty, the planner failed.
    if not plan:
        print("--- EXECUTOR ERROR: No plan provided by Planner ---")
        return {
            "errors": ["Planner failed to generate search categories."],
            "iteration_count": current_count + 1
        }

    # 2. Execution Loop
    for category in plan:
        try:
            print(f"--- EXECUTOR: Fetching news for '{category}' ---")
            # C2SI Standard: Use .invoke() for tool-calling compatibility
            news = fetch_cyber_news.invoke(category)
            
            if news and isinstance(news, list):
                current_results.extend(news)
            else:
                print(f"--- EXECUTOR: No results for {category} ---")
                
        except Exception as e:
            print(f"--- EXECUTOR TOOL ERROR: {str(e)} ---")
            # We don't crash; we log the error in the state
            return {"errors": [f"Tool failure on {category}: {str(e)}"]}

    # 3. State Update (C2SI Professional Standard)
    # Note: We do NOT hardcode "next_step" here anymore. 
    # The Graph (AgentService) decides where to go based on these results.
    return {
        "raw_results": current_results,
        "iteration_count": current_count + 1
    }