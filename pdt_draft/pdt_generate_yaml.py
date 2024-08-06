import os
import yaml
from pathlib import Path

def get_image_paths(folder_path):
    """Get all image paths in the specified folder."""
    image_paths = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_paths.append(os.path.join(folder_path, file))
    return sorted(image_paths)

def generate_yaml(base_path, date):
    full_path = os.path.join(base_path, date)
    data = {
        "title": f"SPY {date[:4]}-{date[4:6]}-{date[6:]}",
        "ticker": "SPY",  # Hardcoded for now, but can be extracted from the folder name
        "date": date,
        "author": "Omar Palomino",
        "summary": f"SPY_{date}_summary.md",
        "sections": []
    }

    graphs_path = os.path.join(full_path, "graficos")
    graphs_section = {"graphs": []}
    graph_order = ["v1d", "ichim", "v5m", "v1m"]

    for prefix in graph_order:
        graph_files = [f for f in get_image_paths(graphs_path) if f"{prefix}" in os.path.basename(f)]
        for image_path in graph_files:
            filename = os.path.basename(image_path)
            graphs_section["graphs"].append(filename)

    data["sections"].append(graphs_section)

    options_path = os.path.join(full_path, "contratos")
    options_section = {"options": []}
    # Sort directories by creation date in descending order
    sorted_folders = sorted(os.listdir(options_path), key=lambda x: os.path.getctime(os.path.join(options_path, x)), reverse=True)

    for option_folder in sorted_folders:
        # Your code here
        option_path = os.path.join(options_path, option_folder)
        if os.path.isdir(option_path):
            option_data = {option_folder: [os.path.basename(path) for path in get_image_paths(option_path)]}
            options_section["options"].append(option_data)

    data["sections"].append(options_section)

    gammas_path = os.path.join(full_path, "gammas")
    gammas_section = {"gammas": [os.path.basename(path) for path in get_image_paths(gammas_path)]}
    data["sections"].append(gammas_section)

    yaml_file_path = os.path.join(full_path, f"SPY_{date}_summary.yaml")
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)
    print(f"YAML file created: {yaml_file_path}")

if __name__ == "__main__":
    base_path = "/Users/omarps/Library/CloudStorage/OneDrive-Personal/Proyectos/CDI/PDT/2024/2024q3"  # Replace with the path to your base folder
    date = "20240718"  # Replace with the date
    generate_yaml(base_path, date)
