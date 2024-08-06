from PIL import Image
import pytesseract
import re
import os

# Function to extract text from image using OCR
def extract_text_from_image(image_path):
  # Open the image file
  img = Image.open(image_path)

  # Perform OCR on the image
  text = pytesseract.image_to_string(img)

  return text

# Function to parse extracted text and get ticker and contract details
def parse_text_for_details(text):
  # Regular expression patterns to match ticker and contract details

  ticker_pattern = r'(\w+)\s*(\d{4})\s*(\w+)\s*(\d+)\s*(\w+)\s*(\w+)'
  # ticker_pattern = r'Ticker:\s*(\w+)'
  contract_pattern = r'([A-Z]{1,4}\d{6}[CP€]\d{3,})' # TODO: get the target with decimals
  # contract_pattern = r'Contract:\s*(\d{4}-\d{2}-\d{2})\s*(\w+)\s*Target:\s*(\d+)'
  time_pattern = r'(5m|15m|30m|1h|4h|1d)'

  # Try to find matches in the text
  ticker_match = re.search(ticker_pattern, text)
  contract_match = re.search(contract_pattern, text)
  time_match = re.search(time_pattern, text)

  # Extract information
  ticker = ticker_match.group(1) if ticker_match else None

  if contract_match:
    contract_str = contract_match.group(1)
    contract_date_re = r'(\d{6})'
    contract_type_re = r'([CP€])'
    contract_target_re = r'(\d{3,})$'
    contract_date_match = re.search(contract_date_re, contract_str)
    contract_type_match = re.search(contract_type_re, contract_str)
    contract_target_match = re.search(contract_target_re, contract_str)

    contract_date = contract_date_match.group(1) if contract_date_match else None
    contract_type = contract_type_match.group(1) if contract_type_match else None
    contract_target = contract_target_match.group(1) if contract_target_match else None
  else:
    contract_date = None
    contract_type = None
    contract_target = None

  time_frame = time_match.group(1) if time_match else None

  return ticker, contract_date, contract_type, contract_target, time_frame

# Function to rename the file based on extracted details
def rename_file(original_filename, ticker, contract_date, contract_type, contract_target):
  directory = os.path.dirname(original_filename)
  filename, ext = os.path.splitext(original_filename)
  new_filename = f"{ticker}_{contract_date}_{contract_type}_{contract_target}{ext}"
  new_filepath = os.path.join(directory, new_filename)
  # os.rename(original_filename, new_filename)
  os.rename(original_filename, new_filepath)
  print(f"File renamed to: {new_filepath}")

# Function to make a copy of the file based on extracted details
def copy_file(original_filename, ticker, contract_date, contract_type, contract_target):
    directory = os.path.dirname(original_filename)
    filename, ext = os.path.splitext(original_filename)
    new_filename = f"{ticker}_{contract_date}_{contract_type}_{contract_target}{ext}"
    new_filepath = os.path.join(directory, new_filename)
    # os.copy(original_filename, new_filename)
    # print(directory, filename, original_filename, new_filename)
    os.popen(f'cp {original_filename} {new_filepath}')
    print(f"File copied to: {new_filepath}")

if __name__ == "__main__":
  # Get the path of the input image
  image_path = input("Enter the path of the image: ")
  # image_path = '/Users/omarps/Downloads/2024-07-02-TOS_CHARTS-1.png'

  # Extract text from the image
  extracted_text = extract_text_from_image(image_path)

  # Print the extracted text
  print("Extracted text:")
  print(extracted_text)

  # Parse extracted text for details
  ticker, contract_date, contract_type, contract_target, time_frame = parse_text_for_details(extracted_text)

  if ticker and contract_date and contract_type and contract_target and time_frame:
    # Rename the file based on extracted details
    # rename_file(image_path, ticker, contract_date, contract_type, contract_target)
    # Copy the file based on extracted details
    copy_file(image_path, ticker, contract_date, contract_type, contract_target)
  else:
    # Print the parsed details
    print("Parsed details:")
    print(f"Ticker: {ticker}")
    print(f"Contract Date: {contract_date}")
    print(f"Contract Type: {contract_type}")
    print(f"Contract Target: {contract_target}")
    print(f"Time Frame: {time_frame}")
