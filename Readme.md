## UdaPlay: AI Research Agent for the Video Game Industry
### Capstone project for the Udacity Building Agents course.

UdaPlay answers questions about video games. It first searches a local knowledge base (RAG over 15 games), evaluates whether the results are good enough, and only then falls back to a web search. Answers are structured and cite their sources.

### Tools & Purpose
- retrieve_game - Semantic search in the ChromaDB vector store
- evaluate_retrieval - LLM judge that returns whether the documents are useful, a confidence level and an explanation
- game_web_search - Tavily web search, returns page URLs so answers can cite them
The agent is a state machine (lib/state_machine.py) with session memory, so follow-up questions work.

### Project layout
- Udaplay_01_starter_project.ipynb   Part 1: build the vector database
- Udaplay_02_starter_project.ipynb   Part 2: the agent and example queries
- games/                             15 game JSON files
- lib/                               helper library (lib/game_store.py is the vector store manager)

### Setup
- Python 3.11 or later, then pip install -r requirements.txt (and pip install notebook).
- Copy .env.example to .env and fill in OPENAI_API_KEY, OPENAI_BASE_URL and TAVILY_API_KEY.
- Run the notebooks from this folder, in order: Part 1 creates the chromadb/ folder, Part 2 loads it.

### Example queries
Question - Path taken
- When was Pokémon Gold and Silver released?	local dataset
- Which one was the first 3D platformer Mario game?	local dataset
- Was Mortal Kombat X released for PlayStation 5?	web search, cites URL
- What is Rockstar Games working on right now?	web search, cites URLs

### Stand Out features
- Structured JSON output for every answer.
- Persistent long-term memory: facts learned from the web are stored in a separate collection and reused in later sessions.
Web results and LLM wording change between runs. Starter code in lib/ comes from the Udacity course material