from langchain_core.runnables import Runnable

from billing.billing_node import billing_node
from general_question.qna_node import  qna_node
from langgraph.graph import StateGraph
from agent.router import route_node
from agent.state import State





graph = StateGraph(State)
graph.add_node("billing", billing_node)
graph.add_node("qna", qna_node)

# ✅ Let LangGraph internally call `route_node`
graph.set_conditional_entry_point(
    route_node,
    {
        "billing": "billing",
        "qna": "qna"
    }
)

graph.set_finish_point("billing")
graph.set_finish_point("qna")
compiled_graph = graph.compile()
#get_graph = graph.compile()
def get_graph() -> Runnable:
    return compiled_graph  # ✅ Must be compiled

