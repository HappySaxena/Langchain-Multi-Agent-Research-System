# LangChain Multi-Agent Research System

A Streamlit-powered research assistant that uses a multi-agent LangChain workflow to gather web search results, scrape content, write a research report, and critique the final output.

## Key Features

- 🔎 Search Agent: performs web search with Tavily and returns recent, relevant information.
- 📖 Reader Agent: selects a top URL from search results and scrapes content with adaptive extraction.
- ✍️ Writer Agent: composes a structured research report with introduction, findings, conclusion, and sources.
- 📝 Critic Agent: reviews the report and provides a score, strengths, and areas for improvement.

## Project Structure

- `app.py` - Streamlit UI and orchestration for the research workflow.
- `src/pipeline/pipeline.py` - coordinates the multi-agent research pipeline.
- `src/agents/agents.py` - builds the search/reader agents and writer/critic prompt chains.
- `src/tools/tools.py` - defines web search and scraping tools.
- `requirements.txt` - Python dependencies.

## Requirements

- Python 3.11 (recommended)
- A Tavily API key configured in `.env`

## Setup

1. Clone the repository or open this folder in your local environment.
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\\Scripts\\activate     # Windows PowerShell
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file in the repository root with your Tavily API key:

```env
TAVILY_API_KEY=your_api_key_here
```

## Run the App

Launch the Streamlit interface:

```bash
streamlit run app.py
```

Then open the local URL displayed by Streamlit in your browser.

## Usage

1. Enter a research topic in the Streamlit app.
2. Click `Start Research`.
3. Review the generated tabs:
   - Search Results
   - Scraped Content
   - Final Report
   - Critic Feedback

## Notes

- The project currently uses the `llama-3.3-70b-versatile` model via `langchain_groq`.
- The scraping tool tries `trafilatura` first, then `readability`, and finally a raw HTML fallback.
- Search and scraping depend on network access and a valid Tavily API key.

## License

This project is licensed under the terms in `LICENSE`.
