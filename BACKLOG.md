# UdaPlay Backlog

Improvement ideas from the Udacity project review (all criteria passed). Ranked by value first, then effort.
Effort: S = under 1 hour, M = a few hours, L = a day or more.

| # | Item | Why | Effort | Area |
|---|---|---|---|---|
| 1 | Source quality filtering in `game_web_search` | The reviewer's most repeated point. Rockstar and Mortal Kombat X results included YouTube. Prefer official publisher pages, press releases and reference sites; require at least one non-video source for current-events questions. | M | Tools |
| 2 | Move agent code into `lib/udaplay_agent.py` | `UdaPlayAgent`, `UdaPlayState`, `GameAnswer`, `Source` and `LongTermMemoryAgent` live in notebook cells. A module keeps the notebooks as light demos and makes the code testable. | M | Structure |
| 3 | Error handling around the Tavily call | If the web API is down the agent should still return a graceful answer instead of failing. | S | Robustness |
| 4 | Evaluation summary table after the demos | One table with query, used_web_search, confidence, top source and expected path turns the traces into a compact performance report. | S | Reporting |
| 5 | Richer long-term memory metadata | Store original_question, answer_date, source_domain and confidence in `udaplay_learned`. Enables freshness checks and better filtering. | M | Memory |
| 6 | Richer session memory | Keep sources, confidence and the rewritten standalone question per turn, not only the answer text. Improves follow-up accuracy. | S | Memory |
| 7 | Keep raw distance next to the rounded one | `retrieve_game` rounds distances. A `raw_distance` field supports precise routing later. | S | Tools |
| 8 | Retrieval summary table in notebook 1 | Query, top result, distance and expected match, to see retrieval quality at a glance. | S | Reporting |
| 9 | Save JSON output for every example query | Currently only `r3["answer"]` is printed as JSON. Save all runs as JSON artifacts. | S | Output |
| 10 | Use `pathlib.Path` for `games/` and `chromadb/` | Notebooks then run from any working directory. | S | Portability |
| 11 | Log evaluation thresholds and fallback rate | Measure where local retrieval succeeds or fails and how often web search triggers. | M | Rigor |
| 12 | Run every setup cell and save outputs | A few setup cells show no output. Cosmetic, but easier to review. | S | Notebook hygiene |

## Suggested order

1. Quick wins: 3, 6, 7, 12.
2. Quality: 1, then 2.
3. Reporting and rigor: 4, 8, 9, 11.
4. Memory design: 5.

## Reviewer reading list

- Tavily search API (search depth, domain filtering) for item 1
- Chroma query and get guide (filters, richer includes) for items 7 and 11
- OpenAI structured outputs and Pydantic models docs for items 5 and 9
