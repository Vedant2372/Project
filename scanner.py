import os
import time
from Project.config import INCLUDE_DIRS, EXCLUDE_DIR_NAMES, ALLOWED_EXTENSIONS
from Project.utils import is_valid_file, should_exclude

def scan_folders():
    start = time.time()
    seen_paths = set()
    file_paths = []

    for base_dir in INCLUDE_DIRS:
        if not os.path.exists(base_dir):
            print(f"⚠️ Skipping non-existent path: {base_dir}")
            continue

        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), EXCLUDE_DIR_NAMES)]
            for file in files:
                full_path = os.path.join(root, file)
                if full_path in seen_paths:
                    continue
                if is_valid_file(full_path, ALLOWED_EXTENSIONS):
                    seen_paths.add(full_path)
                    file_paths.append(full_path)

    end = time.time()
    print(f"⏱ Scanning completed in {round(end - start, 2)} seconds.")
    return file_paths
