from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import sqlite3
from Project.config import FAISS_INDEX_PATH, EMBEDDING_MODEL_NAME, DB_PATH
from Project.db import get_all_metadata

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def search_documents(query, top_k=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 🔍 1. FTS5 keyword search
    c.execute("""
        SELECT d.path, d.filename, d.filetype, d.modified
        FROM documents d
        JOIN documents_fts f ON d.path = f.path
        WHERE documents_fts MATCH ?
        LIMIT ?
    """, (query, top_k))
    fts_results_raw = c.fetchall()
    conn.close()

    # Convert to dict format and tag as FTS
    fts_results = [{
        "path": r[0],
        "filename": r[1],
        "filetype": r[2],
        "modified": r[3],
        "score": 1.0,  # FTS gets max relevance
        "source": "fts"
    } for r in fts_results_raw]

    # 🧠 2. FAISS semantic fallback
    faiss_results = []
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        query_vec = model.encode([query]).astype("float32")
        D, I = index.search(query_vec, top_k)
        metadata = get_all_metadata()

        for i, distance in zip(I[0], D[0]):
            if i < len(metadata):
                path, filename, filetype, modified = metadata[i]
                faiss_results.append({
                    "path": path,
                    "filename": filename,
                    "filetype": filetype,
                    "modified": modified,
                    "score": float(1 / (1 + distance)),  # inverse distance = relevance
                    "source": "faiss"
                })

    # 🔀 3. Merge and deduplicate (FTS takes priority)
    merged = {r["path"]: r for r in faiss_results}  # start with FAISS
    for r in fts_results:  # overwrite if also in FTS
        merged[r["path"]] = r

    # 🔽 4. Sort by score (FTS = 1.0, FAISS = lower based on distance)
    final_results = sorted(merged.values(), key=lambda x: x["score"], reverse=True)

    return final_results
