import streamlit as st
from src.pipeline.pipeline import run_research_pipeline

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 LangChain Multi-Agent Research System")

st.markdown("""
This application performs research using **four AI agents**:

- 🔎 Search Agent
- 📖 Reader Agent
- ✍️ Writer Agent
- 📝 Critic Agent
""")

st.divider()

# --------------------------------------------------
# Input
# --------------------------------------------------

topic = st.text_input(
    "Enter your research topic",
    placeholder="Example: Quantum Computing in Healthcare"
)

# --------------------------------------------------
# Status Box
# --------------------------------------------------

status_placeholder = st.empty()

status = {
    "search": "⏳",
    "reader": "⏳",
    "writer": "⏳",
    "critic": "⏳",
}


def render_status():
    status_placeholder.markdown(
        f"""
### 🤖 Agent Status

| Agent | Status |
|-------|--------|
| 🔎 Search Agent | {status["search"]} |
| 📖 Reader Agent | {status["reader"]} |
| ✍️ Writer Agent | {status["writer"]} |
| 📝 Critic Agent | {status["critic"]} |
"""
    )


render_status()

# --------------------------------------------------
# Callback from pipeline
# --------------------------------------------------


def update_status(step):

    if step == "search":
        status["search"] = "🔄"

    elif step == "reader":
        status["search"] = "✅"
        status["reader"] = "🔄"

    elif step == "writer":
        status["reader"] = "✅"
        status["writer"] = "🔄"

    elif step == "critic":
        status["writer"] = "✅"
        status["critic"] = "🔄"

    elif step == "done":
        status["critic"] = "✅"

    render_status()


# --------------------------------------------------
# Run Button
# --------------------------------------------------

if st.button("🚀 Start Research", use_container_width=True):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    # Reset status
    status["search"] = "⏳"
    status["reader"] = "⏳"
    status["writer"] = "⏳"
    status["critic"] = "⏳"

    render_status()

    try:

        with st.spinner("Running Multi-Agent Research Pipeline..."):

            state = run_research_pipeline(
                topic=topic,
                status_callback=update_status
            )

        st.success("Research Completed Successfully!")

        st.divider()

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🔎 Search Results",
                "📖 Scraped Content",
                "✍️ Final Report",
                "📝 Critic Feedback",
            ]
        )

        with tab1:
            st.subheader("Search Results")
            st.write(state["search_results"])

        with tab2:
            st.subheader("Reader Agent Output")
            st.write(state["scraped_content"])

        with tab3:
            st.subheader("Research Report")
            st.markdown(state["report"])

        with tab4:
            st.subheader("Critic Feedback")
            st.markdown(state["feedback"])

    except Exception as e:

        st.error("An error occurred while running the pipeline.")
        st.exception(e)

        