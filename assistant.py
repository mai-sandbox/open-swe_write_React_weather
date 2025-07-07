"""Main LangGraph workflow implementation for the weather chatbot."""

from typing_extensions import TypedDict
from typing import Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.messages.utils import add_messages
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tools import get_weather


class State(TypedDict):
    """State for the chatbot conversation."""
    messages: Annotated[list[BaseMessage], add_messages]


def chatbot_node(state: State) -> dict:
    """
    Main chatbot node that processes user messages and generates responses.
    
    Args:
        state: Current conversation state containing messages
        
    Returns:
        Dictionary with the AI response message
    """
    # Initialize Claude LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.7,
        max_tokens=1000
    )
    
    # Bind the weather tool to the LLM
    llm_with_tools = llm.bind_tools([get_weather])
    
    # Get the response from the LLM
    response = llm_with_tools.invoke(state["messages"])
    
    return {"messages": [response]}


def create_weather_assistant():
    """
    Create and compile the LangGraph workflow for the weather assistant.
    
    Returns:
        Compiled LangGraph workflow
    """
    # Create the state graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("tools", ToolNode([get_weather]))
    
    # Add edges
    workflow.add_edge(START, "chatbot")
    
    # Add conditional edges for tool routing
    workflow.add_conditional_edges(
        "chatbot",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        }
    )
    
    # After tools are executed, go back to chatbot
    workflow.add_edge("tools", "chatbot")
    
    # Compile the graph
    return workflow.compile()


# Create the compiled assistant
assistant = create_weather_assistant()


if __name__ == "__main__":
    # Simple test to ensure the assistant compiles without errors
    print("Weather assistant compiled successfully!")
    
    # Example usage
    initial_state = {"messages": [HumanMessage(content="Hello!")]}
    result = assistant.invoke(initial_state)
    print(f"Assistant response: {result['messages'][-1].content}")

