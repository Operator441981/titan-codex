"""
TITAN CODEX MCP Server
Bridges Claude Desktop to the local titan_codex_server_simple.py Flask API.

REQUIRES, running at the same time on the same machine:
1. Ollama running (embeddings + chat models loaded)
2. titan_codex_server_simple.py running on http://localhost:5000
   (start it the normal way: python titan_codex_server_simple.py)

This script does NOT start the Flask server or Ollama for you.
It only talks to them over HTTP. If either is down, every tool call
below will fail with a connection error - that's expected, not a bug
in this file.
"""

from mcp.server.fastmcp import FastMCP
import requests

API_URL = "http://localhost:5000/api"
TIMEOUT = 30  # seconds - embedding calls to Ollama can be slow on first load

mcp = FastMCP("titan-codex")


@mcp.tool()
def codex_search(query: str, n_results: int = 5, tag_filter: str = "") -> dict:
    """
    Search TITAN CODEX for soul boxes semantically related to a query.
    Uses embedding similarity, not exact text match.

    Args:
        query: What to search for.
        n_results: Max number of results to return (default 5).
        tag_filter: Optional - only return boxes containing this tag.
    """
    payload = {"query": query, "n_results": n_results}
    if tag_filter:
        payload["tag_filter"] = tag_filter
    try:
        resp = requests.post(f"{API_URL}/search", json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"CODEX server unreachable: {e}"}


@mcp.tool()
def codex_store(title: str, content: str, tags: list[str] = []) -> dict:
    """
    Store a new soul box (a note / context entry) in TITAN CODEX.

    Args:
        title: Short title for the entry.
        content: The full text content to store.
        tags: List of tag strings for later filtering.
    """
    payload = {"title": title, "content": content, "tags": tags}
    try:
        resp = requests.post(f"{API_URL}/store", json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"CODEX server unreachable: {e}"}


@mcp.tool()
def codex_get(box_id: str) -> dict:
    """
    Fetch one soul box by its exact ID. Direct lookup, no embedding call,
    so this works even if Ollama is briefly unresponsive.

    Args:
        box_id: Exact box ID, e.g. 'box_20260710_143210'.
    """
    try:
        resp = requests.get(f"{API_URL}/get/{box_id}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"CODEX server unreachable: {e}"}


@mcp.tool()
def codex_list() -> dict:
    """List every soul box currently stored in TITAN CODEX, newest first."""
    try:
        resp = requests.get(f"{API_URL}/list", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"CODEX server unreachable: {e}"}


@mcp.tool()
def codex_stats() -> dict:
    """Get TITAN CODEX statistics: total boxes, total words, unique tags."""
    try:
        resp = requests.get(f"{API_URL}/stats", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"CODEX server unreachable: {e}"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
