from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from typing import TypedDict, Dict, Any, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import json

# --- Load environment variables ---
load_dotenv()

# --- Setup Database ---
db = SQLDatabase.from_uri("sqlite:///database/nobrokerage_properties.db")

# --- Define Graph State ---
class GraphState(TypedDict):
    question: Annotated[list[BaseMessage], add_messages]
    query: str
    result: str
    answer: str

# --- Initialize LLMs ---
llm_query = init_chat_model(
    model="gemini-2.0-flash",
    temperature=0,
    model_provider="google_genai",
    model_kwargs={"response_format": {"type": "json_object"}}
)

llm_answer = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.6
)

# --- Node 1: Generate SQL Query ---
def generate_query(state: GraphState) -> Dict[str, str]:
    question = state["question"]
    schema = db.get_table_info()

    prompt = PromptTemplate.from_template(
        """
        You are an expert SQL generator.
        Based on the given SQLite database schema, write a valid SQL query to answer the user's question.

        Return in JSON format:
        {{
            "query": "<SQL query>"
        }}

        Schema:
        {schema}

        Question: {question}
        """
    )
    
    query_prompt = prompt.format(schema=schema, question=question)
    response = llm_query.invoke(query_prompt).content.strip("```json\n").strip("\n```")
    

    # Safely parse JSON; fallback to raw response if parsing fails
    try:
        query = json.loads(response).get("query", response)
    except json.JSONDecodeError:
        query = response


    return {"query": query}

# --- Node 2: Execute SQL Query ---
def execute_query(state: GraphState) -> Dict[str, Any]:
    
    query = state.get("query", "")
    if not query:
        return {"result": "No SQL query provided."}

    try:
        result = db.run(query)
    except Exception as e:
        result = f"Error executing query: {e}"
    
    return {"result": result}

# --- Node 3: Generate Natural-Language Answer ---
def generate_answer(state: GraphState) -> Dict[str, str]:
    
    question = state.get("question", "")
    result = state.get("result", "")

    prompt = PromptTemplate.from_template(
        """
        You are frindly and helpful data assistant.
        Based on the SQL query result below, answer the user's question clearly and concisely.
        if the result is empty or does not contain relevant information, respond with "No properties available currently for the given information".
        Provide the answer in a conversational manner, keep response under 6-8 lines maximum.

        Question: {question}
        Result: {result}
        """
    )

    answer_prompt = prompt.format(question=question, result=result)
    answer = llm_answer.invoke(answer_prompt).content.strip()
    
    return {"answer": answer}
