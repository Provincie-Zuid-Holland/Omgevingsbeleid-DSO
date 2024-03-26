import os
import shutil


def create_normalized_path(base_dir, resource_file):
    normalized_base_dir = os.path.normpath(base_dir)
    normalized_resource_file = os.path.normpath(resource_file)

    path = os.path.join(normalized_base_dir, normalized_resource_file)
    return path


def empty_directory(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))
