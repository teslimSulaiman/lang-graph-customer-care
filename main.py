import streamlit as st
from billing.billing_node import list_tables, billing_node
from billing.billing_seeder import BillingSeeder
from agent.router import route_node
from general_question.qna_seeder import QnaSeeder
from general_question.qna_node import qna_node
import streamlit as st
from agent.graph import get_graph
from agent.state import State


# Seed the database at startup
seeder = BillingSeeder()
seeder.run()
seeder.close()

seeder = QnaSeeder()
seeder.run()

st.title("Billing Dashboard")
st.write("Database is seeded and ready.")
st.write(list_tables())
#st.write(billing_node(State(input="هل لدى المعرّف 1 حالة معلّقة")))
my_input = "ما هو مبلغ المستخدم 1؟"
my_input2="هل يمكنني استخدامه على الهواتف المحمولة؟"
st.write(route_node(State(input=my_input2)))
graph = get_graph()
image = graph.get_graph().draw_mermaid_png()

# Display the image in Streamlit
st.image(image, caption="LangGraph Flow")
message = graph.invoke(State(input=my_input2))
st.write(message)
for my_message in message:
    st.write(my_message)
#seeder = QnaSeeder()
#seeder.run()
#vectorstore = seeder.load_vectorstore()
#st.write(qna_node(State(input="هل يمكنني استخدامه على الهواتف المحمولة؟")))



