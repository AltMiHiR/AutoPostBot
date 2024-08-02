import os
import shutil

def remove_pycache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"Removed __pycache__ at: {pycache_path}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    remove_pycache(current_directory)