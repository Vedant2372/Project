from Project.scanner import scan_folders
from Project.embedder import parse_and_embed
from Project.indexer import index_documents
from Project.db import init_db, insert_metadata
from Project.search import search_documents

def run_initial_scan():
    print("🔍 Scanning folders...")
    paths = scan_folders()
    print(f"✅ Found {len(paths)} valid files for processing.\n")


    print("📄 Parsing and embedding...")
    docs = parse_and_embed(paths)

    print("📦 Indexing documents...")
    index_documents(docs)

    print("🗃️ Saving metadata...")
    insert_metadata(docs)

def run_search():
    query = input("🔎 Enter your search query: ")
    results = search_documents(query)
    if not results:
        print("⚠️ No results found.")
        return
    print("\n📁 Search Results:")
    for r in results:
        modified_str = str(r["modified"]).split(".")[0]  # remove microseconds
        filetype = r["filetype"].replace(".", "").capitalize()
        print(f"📄 Name     : {r['filename']}")
        print(f"📁 Path     : {r['path']}")
        print(f"🕒 Modified : {modified_str}")
        print(f"📦 Type     : {filetype}\n")

if __name__ == "__main__":
    init_db()
    run_initial_scan()
    while True:
        run_search()
