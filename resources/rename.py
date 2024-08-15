import os
import re
import datetime


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

def _rename_other_files(base_path, ticker="SPY", dry_run=True):
    # TODO: move to constants
    # TODO: same logic that screenshots
    folder_path = os.path.join(base_path, 'others')
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
        if 'others' in file:
            continue

        # Define the regex pattern to match the date and time in the filename
        pattern = r'IMG_(\d)'
        match = re.match(pattern, file)

        if match:
            # get creation date from file
            creation_time = os.path.getctime(original_filepath)
            formatted_creation_time = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d_%H-%M-%S")
            # Construct new filename
            new_filename = f"{ticker}_other_{formatted_creation_time}_{file}"
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

    # Rename other files
    _rename_other_files(base_path, ticker, dry_run)
