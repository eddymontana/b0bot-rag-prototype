from langgraph.graph import StateGraph, START, END
from services.AgentState import AgentState
from services.PlannerNode import planner_node
from services.ExecutorNode import executor_node
from services.SummarizerNode import summarizer_node

workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("summarizer", summarizer_node)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "summarizer") # Ensure this exists!
workflow.add_edge("summarizer", END)

app_graph = workflow.compile()