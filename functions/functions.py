import os


def subfolders(path="input"):
    """
    Return a list of folder names inside the given path.
    """
    try:
        cwd = os.getcwd()
        path = os.path.join(cwd, path)
        print([
            name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))
        ]
        )
        return [
            name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))
        ]
    except FileNotFoundError:
        print(f"Error: directory '{path}' does not exist.")
        return []

def chunk_list(lst, n):
    """Split list into chunks of size n"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]