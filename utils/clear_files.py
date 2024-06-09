from pathlib import Path

def clear_files(*file_paths):
    print("cleaning up...")
    for file_path in file_paths:
        path = Path(file_path)
        if path.is_file():
            path.write_text('')
            print(f"Cleared contents of {path}")
        else:
            print(f"File {path} does not exist")
