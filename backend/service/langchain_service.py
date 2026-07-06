import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Load .env
env_path = Path(__file__).resolve().parent.parent /".env"
load_dotenv(dotenv_path=env_path)

print("ENV PATH:", env_path)
print("API Key:", os.getenv("GROQ_API_KEY"))
# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5,
)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful career guidance assistant."),
        ("placeholder", "{chat_history}"),
        ("human", "{user_query}"),
    ]
)

chain = prompt | llm

# Chat History Store
store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chat = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_history,
    input_messages_key="user_query",
    history_messages_key="chat_history",
)


class LangChainService:

    def chat_without_memory(self, message: str):
        return llm.invoke(message).content
from fastapi import HTTPException
from groq import AuthenticationError

class LangChainService:

    def chat_without_memory(self, message: str):
        return llm.invoke(message).content

    def chat_with_memory(self, message: str, session_id: str):
        try:
            response = chat.invoke(
                {"user_query": message},
                config={"configurable": {"session_id": session_id}},
            )
            return response.content

        except AuthenticationError:
            raise HTTPException(
                status_code=401,
                detail="Invalid Groq API Key"
            )

    def clear_history(self, session_id: str):
        if session_id in store:
            del store[session_id]
    def clear_history(self, session_id: str):
        if session_id in store:
            del store[session_id]


service = LangChainService()