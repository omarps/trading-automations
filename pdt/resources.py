import os
import re
import datetime
import shutil
from PIL import Image

def _rename_graph_files(base_path, ticker="SPY", dry_run=True):
    folder_path = os.path.join(base_path, 'graficos')
    # Iterate over each directory in the base path
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Get the full file path
            original_filepath = os.path.join(root, file)

            # Extract folder name
            folder_name = os.path.basename(root)

            # Skip if filename contains the folder name already
            if folder_name in file:
                continue

            # Split filename into parts
            filename, ext = os.path.splitext(file)
            parts = filename.split('_')
            if len(parts) < 3:
                continue  # Skip files that don't match the expected pattern

            ticker = parts[0]
            date_time = '_'.join(parts[1:])

            # Construct new filename with folder name included
            new_filename = f"{ticker}_{folder_name}_{date_time}{ext}"
            new_filepath = os.path.join(root, new_filename)

            if dry_run:
                # Print the proposed new filename
                print(f"Would rename: {original_filepath} to {new_filepath}")
            else:
                # Rename the file
                os.rename(original_filepath, new_filepath)
                print(f"Renamed: {original_filepath} to {new_filepath}")

def _rename_option_contracts_files(base_path, ticker="SPY", dry_run=True):
    folder_path = os.path.join(base_path, 'contratos')
    # Iterate over each directory in the base path
    for root, dirs, files in os.walk(folder_path):
        # Only process if there are files in the current directory
        if files:
            # Sort files to ensure consistent incremental numbering
            files.sort()
            for idx, file in enumerate(files, start=1):
                # Get the full file path
                original_filepath = os.path.join(root, file)

                # Skip directories and only process files
                if not os.path.isfile(original_filepath):
                    continue

                # Extract the folder name
                folder_name = os.path.basename(root)

                # Define the pattern to extract the date from the filename
                pattern = r'(\d{4}-\d{2}-\d{2})'
                match = re.search(pattern, file)

                if match:
                    date = match.group(1)

                    # Construct new filename with folder name, date, and incremental number
                    new_filename = f"{folder_name}_{date}_{idx}.png"
                    new_filepath = os.path.join(root, new_filename)

                    if dry_run:
                        # Print the proposed new filename
                        print(f"Would rename: {original_filepath} to {new_filepath}")
                    else:
                        # Rename the file
                        os.rename(original_filepath, new_filepath)
                        print(f"Renamed: {original_filepath} to {new_filepath}")

def _rename_gamma_files(base_path, ticker="SPY", dry_run=True):
    folder_path = os.path.join(base_path, 'gammas')
    # Iterate over each file in the folder
    for file in os.listdir(folder_path):
        # Get the full file path
        original_filepath = os.path.join(folder_path, file)

        # Skip directories and only process files
        if not os.path.isfile(original_filepath):
            continue

        # Skip if filename contains the folder name already
        if 'screenshots' in file:
            continue

        # Define the regex pattern to match the date and time in the filename
        pattern = r'Screenshot (\d{4}-\d{2}-\d{2}) at (\d{1,2})\.(\d{2})\.(\d{2})\s([ap]\.m\.)'
        match = re.match(pattern, file)

        # print(match)
        if match:
            date = match.group(1)
            hour = int(match.group(2))
            minute = match.group(3)
            second = match.group(4)
            period = match.group(5)

            # Convert hour to 24-hour format if necessary
            if period == 'p.m.' and hour != 12:
                hour += 12
            elif period == 'a.m.' and hour == 12:
                hour = 0

            # Construct new filename
            new_filename = f"{ticker}_gamma_{date}-{hour:02d}_{minute}_{second}.png"
            new_filepath = os.path.join(folder_path, new_filename)

            # TODO: reuse in strategy
            if dry_run:
                # Print the proposed new filename
                print(f"Would rename: {original_filepath} to {new_filepath}")
            else:
                # Rename the file
                os.rename(original_filepath, new_filepath)
                print(f"Renamed: {original_filepath} to {new_filepath}")

def _rename_screenshot_files(base_path, ticker="SPY", dry_run=True):
    folder_path = os.path.join(base_path, 'screenshots')
    # Iterate over each file in the folder
    for file in sorted(os.listdir(folder_path)):
        # Get the full file path
        original_filepath = os.path.join(folder_path, file)

        # Skip directories and only process files
        if not os.path.isfile(original_filepath):
            continue

        # ignore .DS_Store files
        if file.startswith("."):
            continue

        # Skip if filename contains the folder name already
        if 'screenshots' in file:
            continue

        # Define the regex pattern to match the date and time in the filename
        pattern = r'IMG_(\d)'
        match = re.match(pattern, file)

        if match:
            # get creation date from file
            creation_time = os.path.getctime(original_filepath)
            formatted_creation_time = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d_%H-%M-%S")
            # Construct new filename
            new_filename = f"{ticker}_screenshot_{formatted_creation_time}_{file}"
            new_filepath = os.path.join(folder_path, new_filename)

            if dry_run:
                # Print the proposed new filename
                print(f"Would rename: {original_filepath} to {new_filepath}")
            else:
                # Rename the file
                os.rename(original_filepath, new_filepath)
                print(f"Renamed: {original_filepath} to {new_filepath}")

def rename_files_in_folders(base_path, ticker="SPY", dry_run=True):
    print("Renaming files in folders")

    # Rename graph files
    _rename_graph_files(base_path, ticker, dry_run)

    # Rename option contracts files
    _rename_option_contracts_files(base_path, ticker, dry_run)

    # Rename gamma files
    _rename_gamma_files(base_path, ticker, dry_run)

    # Rename screenshot files
    _rename_screenshot_files(base_path, ticker, dry_run)

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

def rotate_image(input_path, output_path, angle=-90):
    """Rotate the given image and save it to the output path."""
    with Image.open(input_path) as img:
        rotated_img = img.rotate(angle, expand=True)
        rotated_img.save(output_path)
