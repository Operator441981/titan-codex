"""
TITAN CODEX - Local RAG System
Soul Box Storage & Retrieval for AI Context Management

This system uses:
- Ollama for embeddings and generation (100% free, runs locally)
- ChromaDB for vector storage (persistent, no limits)
- Flask for web server (simple, lightweight)
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import chromadb
from chromadb.config import Settings
import ollama
import os
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize ChromaDB (persistent storage)
chroma_client = chromadb.PersistentClient(path="./codex_database")

# Create or get collection
try:
    collection = chroma_client.get_collection(name="soul_boxes")
    print("✅ Loaded existing soul box collection")
except:
    collection = chroma_client.create_collection(
        name="soul_boxes",
        metadata={"description": "TITAN CODEX soul box storage"}
    )
    print("✅ Created new soul box collection")

# Ollama model to use (we'll use a small, fast model)
EMBED_MODEL = "nomic-embed-text"  # Small embedding model (~274MB)
CHAT_MODEL = "llama3.2:3b"  # Small but capable chat model (~2GB)

def get_embedding(text):
    """Generate embedding for text using Ollama"""
    try:
        response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
        return response['embedding']
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return None

def store_soul_box(content, tags, title):
    """Store a soul box in the codex"""
    try:
        # Generate unique ID
        box_id = f"box_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create metadata
        metadata = {
            "title": title,
            "tags": ",".join(tags) if isinstance(tags, list) else tags,
            "timestamp": datetime.now().isoformat(),
            "word_count": len(content.split())
        }
        
        # Get embedding
        embedding = get_embedding(content)
        if not embedding:
            return {"success": False, "error": "Failed to generate embedding"}
        
        # Store in ChromaDB
        collection.add(
            ids=[box_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )
        
        print(f"✅ Stored soul box: {title} ({box_id})")
        return {"success": True, "id": box_id, "metadata": metadata}
        
    except Exception as e:
        print(f"❌ Storage error: {e}")
        return {"success": False, "error": str(e)}

def search_soul_boxes(query, n_results=5, tag_filter=None):
    """Search for relevant soul boxes"""
    try:
        # Generate query embedding
        query_embedding = get_embedding(query)
        if not query_embedding:
            return {"success": False, "error": "Failed to generate query embedding"}
        
        # Build where filter for tags if provided
        where_filter = None
        if tag_filter:
            where_filter = {"tags": {"$contains": tag_filter}}
        
        # Search in ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        # Format results
        formatted_results = []
        if results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "similarity": 1 - results['distances'][0][i] if 'distances' in results else None
                })
        
        print(f"✅ Found {len(formatted_results)} soul boxes for query: {query}")
        return {"success": True, "results": formatted_results}
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return {"success": False, "error": str(e)}

def list_all_boxes():
    """List all stored soul boxes"""
    try:
        results = collection.get()
        
        boxes = []
        if results['ids']:
            for i in range(len(results['ids'])):
                boxes.append({
                    "id": results['ids'][i],
                    "title": results['metadatas'][i].get('title', 'Untitled'),
                    "tags": results['metadatas'][i].get('tags', ''),
                    "timestamp": results['metadatas'][i].get('timestamp', ''),
                    "word_count": results['metadatas'][i].get('word_count', 0)
                })
        
        # Sort by timestamp (newest first)
        boxes.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {"success": True, "boxes": boxes, "total": len(boxes)}
        
    except Exception as e:
        print(f"❌ List error: {e}")
        return {"success": False, "error": str(e)}

def delete_soul_box(box_id):
    """Delete a soul box"""
    try:
        collection.delete(ids=[box_id])
        print(f"✅ Deleted soul box: {box_id}")
        return {"success": True}
    except Exception as e:
        print(f"❌ Delete error: {e}")
        return {"success": False, "error": str(e)}

# Flask routes
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('codex.html')

@app.route('/api/store', methods=['POST'])
def api_store():
    """API endpoint to store a soul box"""
    data = request.json
    content = data.get('content', '')
    tags = data.get('tags', [])
    title = data.get('title', 'Untitled Soul Box')
    
    if not content:
        return jsonify({"success": False, "error": "No content provided"})
    
    result = store_soul_box(content, tags, title)
    return jsonify(result)

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint to search soul boxes"""
    data = request.json
    query = data.get('query', '')
    n_results = data.get('n_results', 5)
    tag_filter = data.get('tag_filter', None)
    
    if not query:
        return jsonify({"success": False, "error": "No query provided"})
    
    result = search_soul_boxes(query, n_results, tag_filter)
    return jsonify(result)

@app.route('/api/list', methods=['GET'])
def api_list():
    """API endpoint to list all soul boxes"""
    result = list_all_boxes()
    return jsonify(result)

@app.route('/api/delete', methods=['POST'])
def api_delete():
    """API endpoint to delete a soul box"""
    data = request.json
    box_id = data.get('id', '')
    
    if not box_id:
        return jsonify({"success": False, "error": "No ID provided"})
    
    result = delete_soul_box(box_id)
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API endpoint to get codex statistics"""
    try:
        results = collection.get()
        total_boxes = len(results['ids'])
        
        # Calculate total words stored
        total_words = sum(meta.get('word_count', 0) for meta in results['metadatas'])
        
        # Get unique tags
        all_tags = []
        for meta in results['metadatas']:
            tags_str = meta.get('tags', '')
            if tags_str:
                all_tags.extend(tags_str.split(','))
        unique_tags = list(set(all_tags))
        
        return jsonify({
            "success": True,
            "stats": {
                "total_boxes": total_boxes,
                "total_words": total_words,
                "unique_tags": len(unique_tags),
                "tags": sorted(unique_tags)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔥 TITAN CODEX - Soul Box Storage System")
    print("="*60)
    print(f"📦 Database location: ./codex_database")
    print(f"🤖 Embedding model: {EMBED_MODEL}")
    print(f"💬 Chat model: {CHAT_MODEL}")
    print("="*60)
    print("\n⚡ Starting server on http://localhost:5000")
    print("📝 Open this URL in your browser to use the Codex\n")
    
    # Check if Ollama is running
    try:
        ollama.list()
        print("✅ Ollama is running!\n")
    except:
        print("⚠️  WARNING: Ollama might not be running!")
        print("   Make sure Ollama is installed and running.\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
