import os
import yaml
from md.md_utils import extract_contract_titles
from reports.utils import get_image_paths


def generate_yaml(base_path, date):
    print("Generating YAML file...")
    full_path = os.path.join(base_path, date)
    data = {
        "title": f"SPY {date[:4]}-{date[4:6]}-{date[6:]}",
        "ticker": "SPY",  # Hardcoded for now, but can be extracted from the folder name
        "date": date,
        "author": "Omar Palomino",
        "summary": f"SPY_{date}_summary.md",
        "sections": []
    }

    # Graphs section
    graphs_path = os.path.join(full_path, "graficos")
    graphs_section = {"graphs": []}
    graph_order = ["v1d", "ichim", "v5m", "v1m"]

    for prefix in graph_order:
        graph_files = [f for f in get_image_paths(graphs_path) if f"{prefix}" in os.path.basename(f)]
        for image_path in graph_files:
            filename = os.path.basename(image_path)
            graphs_section["graphs"].append(filename)

    data["sections"].append(graphs_section)

    # Options section
    options_path = os.path.join(full_path, "contratos")
    options_section = {"options": []}

    sorted_folders = extract_contract_titles(os.path.join(full_path, f"SPY_{date}_summary.md"))
    sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))

    for option_folder in sorted_folders:
        option_path = os.path.join(options_path, option_folder)
        if os.path.isdir(option_path):
            option_data = {option_folder: [os.path.basename(path) for path in get_image_paths(option_path)]}
            options_section["options"].append(option_data)

    data["sections"].append(options_section)

    # Gammas section
    gammas_path = os.path.join(full_path, "gammas")
    gammas_section = {"gammas": [os.path.basename(path) for path in get_image_paths(gammas_path)]}
    data["sections"].append(gammas_section)

    # Screenshots section
    screenshots_path = os.path.join(full_path, "screenshots")
    screenshots_section = {"screenshots": [os.path.basename(path) for path in get_image_paths(screenshots_path)]}
    data["sections"].append(screenshots_section)

    yaml_file_path = os.path.join(full_path, f"SPY_{date}_summary.yaml")
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)
    print(f"YAML file created: {yaml_file_path}")
