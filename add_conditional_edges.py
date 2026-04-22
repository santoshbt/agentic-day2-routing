from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
import operator

class SupportState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    should_escalate: bool
    issue_type: str
    user_tier: str

def route_by_tier(state: SupportState) -> str:
    """ Route based on user tier """
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
	# You can call an LLM here if you want.
	# For the assignment it is fine to just set a friendly VIP response.
	return {
		"should_escalate": False,
	}


def standard_agent_node(state: SupportState):
	"""Standard path: may escalate."""
	# For now, just mark should_escalate = True to simulate escalation.
	return {
		"should_escalate": True,
	}

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