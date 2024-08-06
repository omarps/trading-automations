import os
from pathlib import Path

def rename_files_in_folders(base_path, dry_run=True):
  # Iterate over each directory in the base path
  for root, dirs, files in os.walk(base_path):
    for file in files:
      # Get the full file path
      original_filepath = os.path.join(root, file)

      # Extract folder name
      folder_name = os.path.basename(root)

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

# Example usage
if __name__ == "__main__":
  # Path to the base directory containing all the folders
  base_path = "/Users/omarps/Downloads/pdt/graficos"
  rename_files_in_folders(base_path, False)
