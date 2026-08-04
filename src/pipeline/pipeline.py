
from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str, status_callback=None) -> dict:
    state = {}

    def update(step):
        if status_callback:
            status_callback(step)
        else:
            print(step)

    # -------------------- Search --------------------
    update("search")

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    # -------------------- Reader --------------------
    update("reader")

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    # -------------------- Writer --------------------
    update("writer")

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    # -------------------- Critic --------------------
    update("critic")

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    update("done")

    return state

