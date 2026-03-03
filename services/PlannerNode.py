import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from services.AgentState import AgentState

def planner_node(state: AgentState):
    """
    C2SI Planner: Takes a user query and breaks it into 
    specific search categories for the Executor.
    """
    query = state.get("query", "")
    
    llm = ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template(
        "You are a C2SI Security Dispatcher. Given the user request: '{query}', "
        "identify the 3 most relevant search categories from this list: "
        "[malware, cyberAttack, Ransomware, phishing, zero-day]. "
        "Return ONLY a comma-separated list of categories."
    )

    print(f"--- PLANNER: Creating execution plan for '{query}' ---")
    chain = prompt | llm
    response = chain.invoke({"query": query})
    
    # Clean the output into a list
    categories = [c.strip() for c in response.content.split(",")]
    
    return {
        "plan": categories,
        "iteration_count": state.get("iteration_count", 0) + 1
    }