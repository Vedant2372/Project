from sentence_transformers import SentenceTransformer
import os
from datetime import datetime
from Project.config import EMBEDDING_MODEL_NAME
import docx
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def read_file_content(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".pdf":
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = " ".join(page.extract_text() or "" for page in reader.pages)

                if text.strip():
                    return text

                # 🧠 OCR fallback if no text extracted
                try:
                    images = convert_from_path(path)
                    ocr_text = ""
                    for img in images:
                        ocr_text += pytesseract.image_to_string(img)
                    return ocr_text
                except Exception as e:
                    print(f"⚠️ OCR failed for {path}: {e}")
                    return ""

        elif ext == ".docx":
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext in [".txt", ".py", ".java", ".md"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif ext == ".csv":
            try:
                df = pd.read_csv(path)
                return df.to_string()
            except:
                return ""

        elif ext == ".xlsx":
            try:
                df = pd.read_excel(path, engine="openpyxl")
                return df.to_string()
            except:
                return ""

    except Exception as e:
        print(f"⚠️ Failed to read {path}: {e}")
        return ""

    return ""

def parse_and_embed(file_paths):
    documents = []
    for path in file_paths:
        content = read_file_content(path)
        if content.strip():
            embedding = model.encode(content)
            documents.append({
                "path": path,
                "filename": os.path.basename(path),
                "modified": datetime.fromtimestamp(os.path.getmtime(path)),
                "content": content,
                "embedding": embedding
            })
        else:
            print(f"⚠️ Skipped: {os.path.basename(path)} (empty or unreadable content)")
    return documents
