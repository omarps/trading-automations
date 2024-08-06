import os
import re
import argparse
from datetime import datetime

def rename_files_in_folder(folder_path, ticker, dry_run=True):
  # Iterate over each file in the folder
  for file in os.listdir(folder_path):
    # Get the full file path
    original_filepath = os.path.join(folder_path, file)

    # Skip directories and only process files
    if not os.path.isfile(original_filepath):
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

      if dry_run:
        # Print the proposed new filename
        print(f"Would rename: {original_filepath} to {new_filepath}")
      else:
        # Rename the file
        os.rename(original_filepath, new_filepath)
        print(f"Renamed: {original_filepath} to {new_filepath}")

# Example usage
if __name__ == "__main__":
    base_path = "/Users/omarps/Downloads/pdt/gammas"
    ticker = "SPY"
    # Call the function with the provided arguments
    rename_files_in_folder(base_path, ticker, dry_run=False)
