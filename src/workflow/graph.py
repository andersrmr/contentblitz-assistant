from langgraph.graph import END, START, StateGraph

from agents.quality import quality_node
from agents.research import research_node
from agents.rewrite import rewrite_node
from agents.router import router_node
from agents.strategist import strategist_node
from agents.writer_linkedin import writer_linkedin_node
from app.state import AppState
from workflow.routing import route_after_quality


def build_graph():
    graph = StateGraph(AppState)
    graph.add_node("router", router_node)
    graph.add_node("research", research_node)
    graph.add_node("strategist", strategist_node)
    graph.add_node("writer", writer_linkedin_node)
    graph.add_node("quality", quality_node)
    graph.add_node("rewrite", rewrite_node)

    graph.add_edge(START, "router")
    graph.add_edge("router", "research")
    graph.add_edge("research", "strategist")
    graph.add_edge("strategist", "writer")
    graph.add_edge("writer", "quality")
    graph.add_conditional_edges(
        "quality",
        route_after_quality,
        {"rewrite": "rewrite", "end": END},
    )
    graph.add_edge("rewrite", "quality")
    return graph.compile()


content_marketing_graph = build_graph()
