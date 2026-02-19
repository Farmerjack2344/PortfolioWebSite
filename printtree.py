import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def print_condensed_tree(base_dir, folders_to_check=None):
    for item in os.listdir(base_dir):
        path = os.path.join(base_dir, item)
        if os.path.isdir(path):
            print(f"{item}/")
            if folders_to_check and item in folders_to_check:
                for subitem in os.listdir(path):
                    subpath = os.path.join(path, subitem)
                    if os.path.isdir(subpath):
                        print(f"    {subitem}/")
                    else:
                        print(f"    {subitem}")

# Only show main apps, static, templates, and media
important_dirs = ['Overview', 'Blog', 'PowerFromUndergroundApp', 'media', 'templates', 'static']
print_condensed_tree(BASE_DIR, important_dirs)