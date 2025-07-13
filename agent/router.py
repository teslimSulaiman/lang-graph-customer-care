from agent.state import State
from llm.config import llm



def route_node(state: State) -> str:
    prompt = f"""
You are a router that decides whether a user's question is related to:
- "billing" (like invoices, payment status, amount)
- OR "qna" (like refund policies, support topics, general info)

Only respond with: billing or qna

Question: {state.input}
"""

    decision = llm.invoke(prompt).content
    return decision if decision in ["billing", "qna"] else "qna"  # fallback
