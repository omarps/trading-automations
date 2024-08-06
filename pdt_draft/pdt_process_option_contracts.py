import os
import re
import argparse
from pathlib import Path

def rename_files_in_subfolders(base_path, dry_run=True):
  # Iterate over each directory in the base path
  for root, dirs, files in os.walk(base_path):
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

# Example usage
if __name__ == "__main__":
  base_path = "/Users/omarps/Downloads/pdt/contratos"
  # Call the function with the provided arguments
  rename_files_in_subfolders(base_path, False)
