from typing import List, Dict, Any
import sqlalchemy
from sqlalchemy import create_engine, text
from agent.state import State
from llm.config import llm

engine = create_engine("sqlite:///billing/billing.db", echo=False)

# --- Utility functions ---
def list_tables() -> List[str]:
    inspector = sqlalchemy.inspect(engine)
    return inspector.get_table_names()

def get_table_schema(table_name: str) -> List[Dict[str, Any]]:
    inspector = sqlalchemy.inspect(engine)
    return inspector.get_columns(table_name)

def execute_sql(query: str) -> List[tuple]:
    with engine.begin() as connection:
        return connection.execute(text(query)).fetchall()


def build_schema_description() -> str:
    tables = list_tables()
    schemas = {t: get_table_schema(t) for t in tables}
    return "\n".join(
        f"Table {table}:\n" + "\n".join(
            f" - {col['name']} ({col['type']})" for col in cols
        )
        for table, cols in schemas.items()
    )


def generate_sql(schema_desc: str, question: str) -> str:
    prompt = f"""
You are an expert SQL assistant. Given the database schema below, write a valid SQL query to answer the user's question.

Schema:
{schema_desc}

User question:
{question}

Only return the SQL query without explanation.
"""
    return llm.invoke(prompt).content.strip().strip("```sql").strip("```")


def generate_human_answer(question: str, sql_query: str, result: list) -> str:
    prompt = f"""
Question: {question}
SQL Query: {sql_query}
Result: {result}

Based on the result, give a short, human-readable answer to the question.
"""
    return llm.invoke(prompt).content.strip()


def billing_node(state: State) -> State:
    input_query = state.input
    schema_desc = build_schema_description()

    sql_query = generate_sql(schema_desc, input_query)
    result = execute_sql(sql_query)
    final_answer = generate_human_answer(input_query, sql_query, result)

    return state.model_copy(update={
        "sql_query": sql_query,
        "answer": final_answer,
        "messages": state.messages + [
            {"role": "user", "content": input_query},
            {"role": "assistant", "content": final_answer}
        ]
    })

#