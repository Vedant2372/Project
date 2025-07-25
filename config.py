import os

# 📂 Scan full drives instead of subfolders (avoids duplicates)
INCLUDE_DIRS = [
    "C:\\",
    "D:\\",  # Will be skipped if not present
]

# ❌ System or tool folders to exclude
EXCLUDE_DIR_NAMES = [
    "AppData", "Program Files", "Program Files (x86)", "Windows", "System32",
    "node_modules", ".git", "__pycache__", ".venv", "venv", ".idea", ".vscode", ".gradle",
    ".angular", "build", "dist", "env", ".next", ".cache"
]

# ✅ Allowed file types (documents, code, DBs)
ALLOWED_EXTENSIONS = [
    ".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx",
    ".py", ".java", ".cpp", ".c", ".js", ".ts", ".html", ".css", ".sql",
    ".db", ".sqlite", ".sqlite3"
]

# 📍 Paths for storage
DB_PATH = "metadata.db"
FAISS_INDEX_PATH = "vector_store.index"

# 🤖 Embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
