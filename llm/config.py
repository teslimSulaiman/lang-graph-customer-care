from langchain_openai import ChatOpenAI
import os
from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = "voc-xxx"
os.environ["BASE_URL"] = "https://openai.vocareum.com/v1"
llm = ChatOpenAI(model="gpt-4o-mini",
                 temperature=0,
                 api_key=os.environ["OPENAI_API_KEY"],
                 base_url=os.environ["BASE_URL"],
                 )
text_embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["BASE_URL"],
)
