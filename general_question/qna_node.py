from langchain_core.documents import Document
from langchain.prompts import ChatPromptTemplate
from agent.state import State
from llm.config import llm
from general_question.qna_seeder import QnaSeeder

# Load the vector store


# Define prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "أجب على السؤال التالي بناءً على السياق التالي.\n\n{context}"),
    ("human", "{question}")
])
# Node logic
def qna_node(state: State) -> State:
    seeder = QnaSeeder()
    vectorstore = seeder.load_vectorstore()
    question = state.input

    # Search for relevant documents
    docs: list[Document] = vectorstore.similarity_search(question, k=3)

    # Prepare context string
    context = "\n\n".join([doc.page_content for doc in docs])

    # Run LLM with context + question
    answer: str = llm.invoke(prompt.format(context=context, question=question)).content

    # Update state
    return state.model_copy(update={
        "answer": answer,
        "documents": docs,
        "messages": state.messages + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
    })
