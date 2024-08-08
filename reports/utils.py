import os


def get_image_paths(folder_path):
    """Get all image paths in the specified folder."""
    image_paths = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_paths.append(os.path.join(folder_path, file))
    return sorted(image_paths)
