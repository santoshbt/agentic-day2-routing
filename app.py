from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
import operator


class SupportState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    should_escalate: bool
    issue_type: str
    user_tier: str


def route_by_tier(state: SupportState) -> str:
    """Route based on user tier"""
    if state.get("user_tier") == "vip":
        return "vip_path"
    return "standard_path"


def check_user_tier_node(state: SupportState):
    """Decide if user is VIP or standard (mock implementation)."""
    first_message = state["messages"][0].content.lower()
    if "vip" in first_message or "premium" in first_message:
        return {"user_tier": "vip"}
    return {"user_tier": "standard"}


def vip_agent_node(state: SupportState):
    """VIP path: fast lane, no escalation."""
    return {"should_escalate": False}


def standard_agent_node(state: SupportState):
    """Standard path: may escalate."""
    return {"should_escalate": True}

def build_graph():
    workflow = StateGraph(SupportState)
    workflow.add_node("check_tier", check_user_tier_node)
    workflow.add_node("vip_agent", vip_agent_node)
    workflow.add_node("standard_agent", standard_agent_node)
    workflow.set_entry_point("check_tier")
    workflow.add_conditional_edges(
        "check_tier",
        route_by_tier,
        {
            "vip_path": "vip_agent",
            "standard_path": "standard_agent",
        },
    )
    workflow.add_edge("vip_agent", END)
    workflow.add_edge("standard_agent", END)
    return workflow.compile()

def main() -> None:
    graph = build_graph()

    vip_result = graph.invoke({
        "messages": [HumanMessage(content="I'm a VIP customer, please check my order")],
        "should_escalate": False,
        "issue_type": "",
        "user_tier": "",
    })
    print("VIP result:", vip_result.get("user_tier"), vip_result.get("should_escalate"))

    standard_result = graph.invoke({
        "messages": [HumanMessage(content="Check my order status")],
        "should_escalate": False,
        "issue_type": "",
        "user_tier": "",
    })
    print("Standard result:", standard_result.get("user_tier"), standard_result.get("should_escalate"))


if __name__ == "__main__":
	main()