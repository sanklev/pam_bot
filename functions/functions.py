import os
import sys

PAGE_SIZE = 4


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





def find_files_in_cv_folder(message: str):
    """
    Does the same job as the pathlib version but using the 'os' module.

    Args:
        message (str): The name of the subfolder to search within /CV.
    """
    # Define the file extensions we are looking for
    target_extensions = ('.png', '.jpg', 'jpeg') # endswith() wants a tuple

    # Construct the path in an OS-agnostic way
    # However, the request for a leading '/' is specific.
    if sys.platform == "win32":
        drive = os.path.splitdrive(os.getcwd())[0]
        base_dir = os.path.join(drive + '\\', 'CV', message)
    else: # Linux, macOS, etc.
        base_dir = os.path.join('/', 'CV', message)

    print(f"[*] Searching in target directory: {base_dir}")

    # 1. Check if the directory exists
    if not os.path.isdir(base_dir):
        print(f"[!] Error: The directory '{base_dir}' does not exist or is not a directory.")
        return

    found_files = []
    # 2. Iterate recursively using os.walk()
    # os.walk yields a 3-tuple for each directory it visits:
    # (current_directory_path, list_of_subdirectories, list_of_filenames)
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            # 3. Check if the filename ends with one of our target extensions
            # We use .lower() to make the check case-insensitive
            if filename.lower().endswith(target_extensions):
                # Construct the full path to the file
                full_path = os.path.join(dirpath, filename)
                found_files.append(full_path)
            if filename.lower().endswith(('.txt')):
                pass


    # 4. Print the results
    if found_files:
        print(f"\n[+] Found {len(found_files)} matching files:")
        for file_path in found_files:
            print(f"  - {file_path}")
    else:
        print("\n[-] No files ending with .png, .jpg, or .txt were found.")