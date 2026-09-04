# 🔥 TITAN CODEX - Installation & Usage Guide

## What Is This?
TITAN CODEX is your personal AI knowledge management system. It solves the "context window problem" by letting you store and retrieve conversation history ("soul boxes") instantly with any AI.

**Zero cost. 100% local. Unlimited storage. Works with ANY AI.**

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
   - First command downloads embedding model (~274MB)
   - Second command downloads chat model (~2GB)
   - This takes 5-10 minutes depending on your internet

---

### STEP 2: Install Python Dependencies (2 minutes)

1. **Open Command Prompt as Administrator:**
   - Search "cmd" in Windows
   - Right-click → "Run as administrator"

2. **Navigate to where you saved the TITAN CODEX files:**
   ```
   cd C:\Users\YourName\Downloads\TITAN_CODEX
   ```
   (Replace with your actual path)

3. **Install Python packages:**
   ```
   pip install -r requirements.txt
   ```
   - This installs Flask, ChromaDB, and Ollama Python libraries
   - Takes 2-3 minutes

---

### STEP 3: Start the TITAN CODEX (30 seconds)

1. **Make sure Ollama is running:**
   - Ollama should auto-start after installation
   - You'll see an Ollama icon in your system tray (bottom-right)
   - If not, search "Ollama" and launch it

2. **Run the TITAN CODEX server:**
   ```
   python titan_codex_server.py
   ```

3. **You should see:**
   ```
   🔥 TITAN CODEX - Soul Box Storage System
   ✅ Ollama is running!
   ⚡ Starting server on http://localhost:5000
   ```

4. **Open your browser:**
   - Go to: http://localhost:5000
   - You'll see the TITAN CODEX interface!

---

## 💡 HOW TO USE IT

### STORING A SOUL BOX (Context from conversations)

1. **Have a conversation with any AI** (Claude, ChatGPT, Gemini, etc.)

2. **When you want to save the context, tell the AI:**
   ```
   "Give me a soul box summary of our conversation about [topic]"
   ```

3. **The AI will give you formatted text.** Copy it.

4. **Go to TITAN CODEX in your browser:**
   - Paste the text in "Content"
   - Add a title: "Finance Tracker - Feb 5, 2025"
   - Add tags: "finance, spreadsheet, automation"
   - Click "Store Soul Box"

5. **Done!** Your context is saved forever.

---

### RETRIEVING A SOUL BOX (Getting context back)

**Method 1: Search by topic**
1. Go to TITAN CODEX
2. Enter search query: "finance tracker spreadsheet"
3. Click "Search"
4. Your relevant soul boxes appear!
5. Click "Copy" to get the text
6. Paste into any AI you're using

**Method 2: List all boxes**
1. Click "List All" button
2. See all your stored soul boxes
3. Click "View" to see full content
4. Click "Copy" to grab the text

**Method 3: Filter by tag**
1. Enter tag in "Filter by Tag": "finance"
2. Click "Search"
3. Only boxes with that tag appear

---

## 🎯 YOUR WORKFLOW

### Example: Working on Finance Dashboard

**Day 1 - Initial Build:**
1. Chat with Claude about building finance tracker
2. After 30 minutes: "Claude, give me a soul box of what we built"
3. Claude summarizes: spreadsheet structure, formulas, features
4. Store in CODEX: Title="Finance Tracker Build", Tags="finance,spreadsheet"

**Day 2 - Continue Building:**
1. Open new Claude chat (fresh context)
2. Go to CODEX → Search "finance tracker"
3. Copy the soul box
4. Tell Claude: "Here's what we built yesterday: [paste]"
5. Continue building!

**Day 3 - Add New Features:**
1. CODEX → Search "finance tracker"
2. Copy all relevant boxes
3. Give to Claude
4. Build new features
5. Store new soul box: "Finance Tracker - Added Bill Auto-Deduct"

---

## 📋 ORGANIZING YOUR SOUL BOXES

### Good Tagging Strategy:

**Project Tags:**
- `finance` - Finance dashboard project
- `training` - Training log project
- `codex` - TITAN CODEX development
- `portfolio` - Portfolio pieces

**Type Tags:**
- `code` - Contains code
- `design` - Design decisions
- `bugfix` - Bug fixes and solutions
- `idea` - Future ideas

**Status Tags:**
- `in_progress` - Currently working on
- `complete` - Finished
- `reference` - For future reference

**Example:**
- Title: "Finance Tracker - Auto-Deduct Feature"
- Tags: `finance, code, in_progress, spreadsheet`

---

## 🛠️ TROUBLESHOOTING

### "Ollama is not running" error:
1. Check system tray (bottom-right) for Ollama icon
2. If not there: Search "Ollama" and launch it
3. Wait 10 seconds, then restart TITAN CODEX

### "Failed to generate embedding" error:
1. Make sure you downloaded the models:
   ```
   ollama pull nomic-embed-text
   ollama pull llama3.2:3b
   ```
2. Verify they're installed: `ollama list`

### "Network error" in browser:
1. Make sure Python server is running
2. Check the command prompt - any errors?
3. Try restarting: Ctrl+C to stop, then run again

### Soul boxes not showing up:
1. Click "Refresh" button
2. Check console in browser (F12) for errors
3. Restart the server

---

## 💾 WHERE IS MY DATA STORED?

All your soul boxes are stored in:
```
./codex_database/
```

This folder is in the same directory as your Python script.

**To backup your soul boxes:**
1. Close TITAN CODEX
2. Copy the entire `codex_database` folder
3. Store somewhere safe (external drive, cloud, etc.)

**To restore from backup:**
1. Replace `codex_database` folder with your backup
2. Start TITAN CODEX
3. Everything is back!

---

## 🎨 CONNECTING TO YOUR CENTRAL DASHBOARD

Once you build your main dashboard (next project), you can:

1. **Embed TITAN CODEX as iframe:**
   ```html
   <iframe src="http://localhost:5000" width="100%" height="800px"></iframe>
   ```

2. **Link from dashboard:**
   ```html
   <a href="http://localhost:5000" target="_blank">📚 Open TITAN CODEX</a>
   ```

3. **API Integration:**
   Your dashboard can directly call TITAN CODEX APIs:
   - Store: `POST http://localhost:5000/api/store`
   - Search: `POST http://localhost:5000/api/search`
   - List: `GET http://localhost:5000/api/list`

---

## 🚀 ADVANCED FEATURES (For Later)

### Auto-Store from AI Chats:
You can build a browser extension that:
1. Detects when you're talking to an AI
2. Auto-saves conversations to TITAN CODEX
3. Tags them automatically

### Multi-Format Support:
TITAN CODEX can store:
- Text (what you have now)
- Code snippets (with syntax highlighting)
- Images (converted to text descriptions)
- PDFs (extracted text)
- Links (with summaries)

We'll add these as you need them!

---

## 📊 STATISTICS

TITAN CODEX tracks:
- **Total soul boxes** - How many you've stored
- **Total words** - All text across all boxes
- **Unique tags** - How many different tags you use

This helps you see your knowledge base grow!

---

## 🔒 PRIVACY & SECURITY

**100% Private:**
- Everything runs on YOUR computer
- No data sent to external servers
- No API keys needed
- No internet required (after initial setup)

**Your data is YOURS:**
- Stored locally in `codex_database` folder
- You can backup, move, or delete anytime
- No one can access it but you

---

## 🎯 WHAT'S NEXT?

Now that you have TITAN CODEX working:

1. **Test it out:**
   - Store a soul box from our finance tracker conversation
   - Try searching for it
   - Practice the workflow

2. **Build your habit:**
   - End each AI session by storing a soul box
   - Tag consistently
   - Review your boxes weekly

3. **Integrate with dashboard:**
   - We'll build your central command center next
   - TITAN CODEX will be one module in it
   - Everything connected!

---

## 💬 COMMON COMMANDS

**To start TITAN CODEX:**
```
python titan_codex_server.py
```

**To stop TITAN CODEX:**
- Press `Ctrl+C` in the command prompt

**To check Ollama models:**
```
ollama list
```

**To update Ollama:**
```
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

---

## 🎉 YOU'RE READY!

Your TITAN CODEX is:
- ✅ Free forever
- ✅ Unlimited storage
- ✅ Works with any AI
- ✅ 100% private
- ✅ Portfolio-ready

Start storing your AI conversations and never lose context again!

**Questions? Issues? Let's debug together!**
