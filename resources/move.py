import os
import shutil


def move_or_copy_files(input_path, output_path, operation="copy"):
    if operation == "move":
        # TODO: fix move pdt contents only
        shutil.move(input_path, output_path)
    else:
        shutil.copytree(input_path, output_path, dirs_exist_ok=True)


def _flatten_graph_folder(output_path):
    graficos_folder = os.path.join(output_path, "graficos")

    for root, dirs, files in os.walk(graficos_folder):
        for file in files:
            # ignore .DS_Store files
            if file.startswith("."):
                continue

            # move folder to graficos folder
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(graficos_folder, file)
            shutil.move(file_path, new_file_path)

    # delete empty dirs
    for root, dirs, files in os.walk(graficos_folder):
        for graph_dir in dirs:
            file_path = os.path.join(root, graph_dir)
            if os.path.isdir(file_path):
                # delete dir
                shutil.rmtree(file_path)


# TODO: review move option
def move_and_restructure(input_path, base_path, date, operation="copy"):
    print(f"Moving and restructuring files: {operation}")

    # Create the base output path
    full_output_path = os.path.join(base_path, date)
    # Create the base output directory if it does not exist
    if not os.path.exists(full_output_path):
        os.makedirs(full_output_path)
    # Move or copy the entire input folder to the output folder with the date
    move_or_copy_files(input_path, full_output_path, operation)

    # Flatten the graficos folder
    _flatten_graph_folder(full_output_path)

    print(f"Folder structure moved and restructured at: {full_output_path}")
