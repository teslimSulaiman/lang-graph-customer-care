# ---- Main App Flow ----
from app import seed_data, init_session_state, render_header, display_chat_history, handle_user_input

seed_data()
init_session_state()
graph = render_header()
display_chat_history()
handle_user_input(graph)