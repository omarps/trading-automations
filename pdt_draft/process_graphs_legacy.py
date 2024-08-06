import os
import argparse
from pathlib import Path

# Define the path mappings
path_mappings = {
    'quick': 'v5m',
    'jh': 'v1d'
}

def rename_files_in_folder(folder_path, dry_run=True):
  # Iterate over each file in the folder
  for file in os.listdir(folder_path):
    # Get the full file path
    original_filepath = os.path.join(folder_path, file)

    # Skip directories and only process files
    if not os.path.isfile(original_filepath):
      continue

    # Split filename into parts
    filename, ext = os.path.splitext(file)
    parts = filename.split('_')
    if len(parts) < 4:
      continue  # Skip files that don't match the expected pattern

    ticker = parts[0]
    folder_type = parts[1]
    date_time = '_'.join(parts[2:])

    # Check if folder_type needs to be replaced
    new_folder_type = path_mappings.get(folder_type, folder_type)

    if folder_type == new_folder_type:
      continue
    else:
      print(folder_type, '->', new_folder_type)

    # Construct new filename with folder type replaced
    new_filename = f"{ticker}_{new_folder_type}_{date_time}{ext}"
    new_filepath = os.path.join(folder_path, new_filename)

    if dry_run:
      # Print the proposed new filename
      print(f"Would rename: {original_filepath} to {new_filepath}\n")
    else:
      # Rename the file
      os.rename(original_filepath, new_filepath)
      print(f"Renamed: {original_filepath} to {new_filepath}\n")

if __name__ == "__main__":
  # Path to the base directory containing all the folders
  base_path = "/Users/omarps/Library/CloudStorage/OneDrive-Personal/Proyectos/CDI/PDT/2024/2024q2/graficos"
  rename_files_in_folder(base_path, False)