import os

def is_valid_file(filepath, allowed_extensions):
    ext = os.path.splitext(filepath)[1].lower()
    return ext in allowed_extensions

def should_exclude(path, exclude_dirs):
    return any(excl in path for excl in exclude_dirs)
