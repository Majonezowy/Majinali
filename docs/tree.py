import os

# Folders to skip
SKIP_DIRS = {"__pycache__", ".venv", ".vscode", ".git"}

def print_tree(start_path=".", prefix=""):
    items = sorted(os.listdir(start_path))
    items = [i for i in items if i not in SKIP_DIRS]  # filter ignored dirs

    for i, item in enumerate(items):
        path = os.path.join(start_path, item)
        connector = "└── " if i == len(items) - 1 else "├── "
        print(prefix + connector + item)

        if os.path.isdir(path):
            extension = "    " if i == len(items) - 1 else "│   "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    print(".")
    print_tree(".")
