from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from nobrokerage_agent import  generate_query, execute_query, generate_answer, GraphState


graph = StateGraph(GraphState)

graph.add_node("generate_query", generate_query)
graph.add_node("execute_query", execute_query)
graph.add_node("generate_answer", generate_answer)

graph.add_edge(START, "generate_query")
graph.add_edge("generate_query", "execute_query")
graph.add_edge("execute_query", "generate_answer")
graph.add_edge("generate_answer", END)

checkpointer = InMemorySaver()
app = graph.compile(checkpointer=checkpointer)

