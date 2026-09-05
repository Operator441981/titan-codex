# TITAN CODEX

A personal, self-hosted memory system for AI conversations. Runs entirely on my own hardware — no cloud service, no subscription, no external API costs beyond what's already local.

## Process

I direct this build — the architecture, the decisions, the debugging, understanding why something's broken and what the fix should be. Claude generates code under that direction.

## Why I built this

I built this because of the context window problem with AI in general. Using AI is like reading a book or taking notes in a notebook — it remembers the first page and the last page really well. It's the stuff in the middle that gets mixed up, vague, or lost. That gets worse the longer a conversation runs — on real project work, AI starts to lose the thread, forgets things, or claims it already did something five turns back that it didn't.

The real problem was thread-switching. Trying to compress everything I'd put into one long conversation into a clean summary for a new one was a time sink — I was spending more effort re-explaining myself than doing the actual work. I built CODEX to be an external memory that sits outside any one conversation, so I'm not the one carrying context between threads by hand.

This wasn't an attempt to build a better version of anything Anthropic makes. CODEX was built months before Anthropic shipped native cross-session memory for Claude. It was solving a real, personal problem before a platform solution existed for it. Now the two do different jobs: Claude's built-in memory handles fast session-to-session continuity inside Claude itself. CODEX is broader — it's my own personal knowledge base (projects, career planning, hardware notes, study progress — not just "what did Claude and I talk about"), and it's also just been a way to actually learn Flask, Python, and how a RAG pipeline works by building one instead of only reading about it.

## How it works

Four pieces, in order:

1. **Ollama** — runs the embedding model (`nomic-embed-text`) and a local chat model (`llama3.2:3b`) locally, no API key, no per-call cost.
2. **Flask app** (`titan_codex_server_simple.py`) — the only piece that touches storage. Loads the JSON file, writes to it, and is the thing all requests actually go through.
3. **JSON file** (`codex_database.json`, not included in this repo) — the actual data store. No database engine. Every entry (a "soul box") has a title, content, tags, a timestamp, and an embedding vector.
4. **MCP server** (`codex_mcp_server.py`) — bridges Claude Desktop to the Flask app over local HTTP. This is what lets me just ask Claude in plain language to store or search something, instead of hitting the API by hand. Search and retrieval are always available; storing something new requires my approval first — a deliberate boundary, not a limitation.

Search works by cosine similarity: a query gets embedded the same way stored entries were, and the system returns whatever's closest in meaning, not keyword overlap. Two entries can share the exact same word and be about completely unrelated things — this compares the vectors, not the text.

## Why JSON instead of a real database

At my current entry count, I don't need concurrency or enterprise-grade anything — this is single-user, single-machine. JSON meant zero setup dependencies and a file I can open and read directly. The tradeoff is scalability: it's a full linear scan on every search. Known limitation, not a surprise — a real database migration is a planned future step, not urgent yet.

## Keeping track of entries

I also keep a separate log of every entry stored — what it's about and when — as a quick index without having to open the full JSON file. It's not included in this repo since it lists actual entry titles and topics from my personal/project work, but the mechanism is simple: every store operation gets a corresponding row logged alongside it.

## Recent fixes (Aug 30, 2026)

Two real bugs found and fixed in `titan_codex_server_simple.py`:

**Security exposure.** The server was running `app.run(debug=True, host='0.0.0.0', port=5000)`. `host='0.0.0.0'` bound it to every network interface — reachable from any device on the home network, not just this machine. `debug=True` enables Werkzeug's interactive debugger, which gives a live Python console at any unhandled error — real code-execution risk if reachable. Fixed to `debug=False`, `host='127.0.0.1'`. Verified zero functional impact first: the MCP bridge only ever calls `localhost:5000`, confirmed by reading that file before making the change.

**Data-quality bug.** `store_soul_box()` split tags with `tags.split(',')` and never stripped whitespace. Anything saved through the web UI as `"TITAN, ESTIMATOR"` stored the second tag as `" ESTIMATOR"` — leading space baked in as a literal character. Since tag search does an exact match, searching `"ESTIMATOR"` silently never matched it. No crash, no error — it just quietly returned nothing. Fixed to strip each tag: `[t.strip() for t in tags.split(',')]`. Forward-only — doesn't retroactively clean tags already stored before the fix.

## Status

`codex_database.json` and the entry log both hold real personal and project content and will never be published, regardless of what happens with the rest of this code. Both are excluded via `.gitignore`.

## Stack

Python, Flask, Ollama (`nomic-embed-text`, `llama3.2:3b`), JSON file storage, MCP (Model Context Protocol) bridge to Claude Desktop. No cloud dependency, no external database.
