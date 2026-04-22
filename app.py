from langchain_core.messages import HumanMessage
from add_conditional_edges import build_graph

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