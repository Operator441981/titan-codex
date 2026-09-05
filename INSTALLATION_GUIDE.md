# 🔥 TITAN CODEX - Installation & Usage Guide

## What Is This?
TITAN CODEX is your personal AI knowledge management system. It solves the "context window problem" by letting you store and retrieve conversation history ("soul boxes") instantly with any AI.

**Zero cost. 100% local. Unlimited storage (JSON file, no external database). Works with any AI that supports MCP, or manually with any AI via copy/paste.**

---

## 🚀 INSTALLATION (20 Minutes)

### STEP 1: Install Ollama (5 minutes)

Ollama runs AI models locally on your machine - no API keys, no costs, no limits.

1. **Download Ollama for Windows:**
   - Go to: https://ollama.com/download
   - Click "Download for Windows"
   - Run the installer (OllamaSetup.exe)
   - Follow the prompts (just keep clicking Next)

2. **Verify Ollama is installed:**
   - Open Command Prompt (search "cmd" in Windows)
   - Type: `ollama --version`
   - You should see a version number

3. **Download the AI models:**
   ```
   ollama pull nomic-embed-text
   ollama pull llama3.2:3b
   ```
   - First command downloads the embedding model (~274MB) - used for semantic search
   - Second command downloads the chat model (~2GB)
   - This takes 5-10 minutes depending on your internet

---

### STEP 2: Install Python Dependencies (2 minutes)

1. **Open Command Prompt or PowerShell:**
   - Search "cmd" or "PowerShell" in Windows

2. **Navigate to where you saved the TITAN CODEX files:**
   ```
   cd C:\Users\YourName\Downloads\TITAN_CODEX
   ```
   (Replace with your actual path)

3. **Install Python packages:**
   ```
   pip install -r requirements.txt
   ```
   - This installs Flask, Flask-CORS, the Ollama Python client, NumPy, and Requests
   - No database engine required - storage is a plain JSON file
   - Takes 1-2 minutes

---

### STEP 3: Start the TITAN CODEX server (30 seconds)

1. **Make sure Ollama is running:**
   - Ollama should auto-start after installation
   - You'll see an Ollama icon in your system tray (bottom-right)
   - If not, search "Ollama" and launch it

2. **Run the TITAN CODEX server:**
   ```
   python titan_codex_server_simple.py
   ```

3. **You should see the server start up and confirm Ollama is reachable**, then it will be listening on `http://127.0.0.1:5000` (localhost only - not reachable from other devices on your network by design).

4. **Open your browser:**
   - Go to: http://localhost:5000
   - You'll see the TITAN CODEX interface (Store / Retrieve / Results)

---

### STEP 4 (Optional): Connect it to Claude Desktop via MCP

If you want to talk to CODEX in plain language through Claude Desktop instead of using the web UI directly:

1. Make sure `titan_codex_server_simple.py` is running (Step 3) and Ollama is running.
2. Add `codex_mcp_server.py` to your Claude Desktop MCP config (`claude_desktop_config.json`), pointing at this script's path on your machine.
3. Restart Claude Desktop. You should now have access to five tools: `codex_search`, `codex_store`, `codex_get`, `codex_list`, `codex_stats`.
4. The MCP server talks to the Flask app over `http://localhost:5000` - it does not replace or duplicate the Flask server, it's a thin bridge on top of it. Both need to be running for this to work.

---

## 💡 HOW TO USE IT

### STORING A SOUL BOX (Context from conversations)

1. **Have a conversation with any AI** (Claude, ChatGPT, Gemini, etc.)

2. **When you want to save the context, ask the AI to summarize it** in a clear format - topic, decisions made, open questions, anything you'd want to pick back up later.

3. **Copy that summary.**

4. **Go to TITAN CODEX in your browser (or use the `codex_store` MCP tool if connected to Claude Desktop):**
   - Paste the text in "Content"
   - Add a title: e.g. "Finance Tracker - Feb 5"
   - Add tags: e.g. "finance, spreadsheet, automation"
   - Click "Store Soul Box"

5. **Done.** Your context is saved to `codex_database.json` on your machine.

---

### RETRIEVING A SOUL BOX (Getting context back)

**Method 1: Semantic search**
1. Go to TITAN CODEX (or use `codex_search` via Claude Desktop)
2. Enter a search query, e.g. "finance tracker spreadsheet"
3. Click "Search"
4. Results are ranked by meaning (cosine similarity on the embedding), not exact keyword match
5. Click "Copy" to get the text, paste into any AI you're using

**Method 2: List all boxes**
1. Click "List All" (or use `codex_list`)
2. See every stored soul box, newest first
3. Click "View" to see full content, "Copy" to grab the text

**Method 3: Filter by tag**
1. Enter a tag in "Filter by Tag", e.g. "finance"
2. Click "Search" - only boxes with that tag appear

---

## 🎯 YOUR WORKFLOW

### Example: Working on a multi-day project

**Day 1 - Initial Build:**
1. Chat with an AI about building something
2. Near the end of the session, ask for a summary of what was built/decided
3. Store it in CODEX: Title="Finance Tracker Build", Tags="finance,spreadsheet"

**Day 2 - Continue Building:**
1. Open a new chat (fresh context, no memory of Day 1)
2. Search CODEX for "finance tracker"
3. Paste the retrieved summary into the new chat
4. Continue building with full context restored

**Day 3 - Add New Features:**
1. Search CODEX for relevant prior entries
2. Give them to the AI
3. Store a new soul box documenting what changed

---

## 📋 ORGANIZING YOUR SOUL BOXES

### Tagging strategy that actually holds up over time:

**Project tags** - what it's for (e.g. `finance`, `codex`, `vm-lab`)

**Type tags** - what kind of content it is (e.g. `code`, `bugfix`, `idea`, `session-log`)

**Status tags** - where it stands (e.g. `in-progress`, `complete`, `reference`)

**Example:**
- Title: "Finance Tracker - Auto-Deduct Feature"
- Tags: `finance, code, in-progress`

---

## 🛠️ TROUBLESHOOTING

### "CODEX server unreachable" (from an MCP tool call):
1. Confirm `titan_codex_server_simple.py` is actually running in a terminal
2. Confirm Ollama is running (check the system tray)
3. Confirm nothing else is using port 5000

### "Failed to generate embedding" error:
1. Make sure both models are downloaded:
   ```
   ollama pull nomic-embed-text
   ollama pull llama3.2:3b
   ```
2. Verify they're installed: `ollama list`

### Soul boxes not showing up in the UI:
1. Click "Refresh"
2. Check the browser console (F12) for errors
3. Restart the server

---

## 💾 WHERE IS MY DATA STORED?

Everything is stored in a single file:
```
codex_database.json
```
in the same directory as the Python scripts.

**This file is never committed to this repository** (see `.gitignore`) - it's excluded on purpose because it holds real personal and project content.

**To back up your soul boxes:** copy `codex_database.json` somewhere safe (external drive, cloud storage, etc.) while the server is stopped.

**To restore from backup:** replace `codex_database.json` with your backup copy, then start the server.

---

## 🔒 PRIVACY & SECURITY

**Local by design:**
- Everything runs on your own machine - Ollama, the Flask server, and the JSON data store
- No data sent to external servers, no API keys needed
- The server is bound to `127.0.0.1` (localhost only) - it is not reachable from other devices on your network, and definitely not from the internet, unless you deliberately reconfigure it to be

**Your data is yours:**
- Stored locally in `codex_database.json`
- Back it up, move it, or delete it any time
- Nobody else can read it unless they have access to your machine

---

## 🎉 YOU'RE READY

Clone this repo, follow Steps 1-3, and you have your own local AI memory system running in about 20 minutes. Step 4 is optional if you want to talk to it through Claude Desktop instead of the web UI.

**Found a bug or have a question? Open an issue on this repo.**
