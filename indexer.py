import faiss
import numpy as np
import os
from Project.config import FAISS_INDEX_PATH

def index_documents(docs):
    dim = len(docs[0]["embedding"])
    index = faiss.IndexFlatL2(dim)
    vectors = np.array([doc["embedding"] for doc in docs]).astype("float32")
    index.add(vectors)
    faiss.write_index(index, FAISS_INDEX_PATH)
    print(f"✅ Indexed {len(docs)} documents")
