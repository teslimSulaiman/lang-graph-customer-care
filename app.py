from billing.billing_seeder import BillingSeeder
from general_question.qna_seeder import QnaSeeder
import streamlit as st
from agent.graph import get_graph
from agent.state import State

# Seed the database at startup
seeder = QnaSeeder()
seeder.run()

seeder = BillingSeeder()
seeder.run()
seeder.close()

graph = get_graph()
image = graph.get_graph().draw_mermaid_png()

# Display the image in Streamlit
st.image(image, caption="LangGraph Flow")

st.set_page_config(page_title="AI Agent Chat", layout="centered")
st.title("🤖 AI Assistant")
st.caption("Ask me about billing or general topics.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "state" not in st.session_state:
    st.session_state.state = State(input="", messages=[], answer="", documents=[])

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("اكتب سؤالك هنا... (Type your question here)")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create new state with user input
    current_state = st.session_state.state.model_copy(update={"input": user_input})
    new_state_dict = graph.invoke(current_state)
    new_state = State(**new_state_dict)
    st.session_state.state = new_state

    # Get answer
    assistant_response = new_state.answer

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Update chat history
    st.session_state.messages.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": assistant_response}
    ])

    st.session_state.state = new_state
