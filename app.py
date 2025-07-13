import streamlit as st
from billing.billing_seeder import BillingSeeder
from general_question.qna_seeder import QnaSeeder
from agent.graph import get_graph
from agent.state import State

def seed_data():
    """Seed vector and SQL databases only once per session."""
    if st.session_state.get("seeded"):
        return

    QnaSeeder().run()
    billing_seeder = BillingSeeder()
    billing_seeder.run()
    billing_seeder.close()

    st.session_state.seeded = True

def init_session_state():
    """Initialize Streamlit session state values."""
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("state", State(input="", messages=[], answer="", documents=[]))

def render_header():
    """Render title, caption, and graph image."""
    st.set_page_config(page_title="AI Agent Chat", layout="centered")
    st.title("🤖 AI Assistant")
    st.caption("Ask me about billing or general topics.")

    graph = get_graph()
    image = graph.get_graph().draw_mermaid_png()
    st.image(image, caption="LangGraph Flow")

    return graph

def display_chat_history():
    """Display the conversation history."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_user_input(graph):
    """Handle the user input and update state accordingly."""
    user_input = st.chat_input("اكتب سؤالك هنا... (Type your question here)")
    if not user_input:
        return

    with st.chat_message("user"):
        st.markdown(user_input)

    current_state = st.session_state.state.model_copy(update={"input": user_input})
    new_state_dict = graph.invoke(current_state)
    new_state = State(**new_state_dict)

    assistant_response = new_state.answer
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    st.session_state.messages.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": assistant_response}
    ])
    st.session_state.state = new_state

