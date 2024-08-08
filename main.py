import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from folders import options
from resources import files
from reports import generate


load_dotenv()


if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")

    # Get parameters from environment variables
    input_path = os.getenv("INPUT_PATH")
    base_path = os.getenv("BASE_PATH")
    ticker = os.getenv("TICKER")
    dry_run = os.getenv("DRY_RUN").lower() == 'true'

    # Ask for which option to run and execute per module
    option = input(
        "Which option do you want to run?\n"
        "1: Folder Options\n"
        "2: Files Options\n"
        "3: Report Options\n"
    )

    # Add modules here
    if option == "1":
        # 1. Folders options
        options.run()
    elif option == "2":
        # 2. Files options
        files.run()
    elif option == "3":
        # 3. Report options
        generate.run()
    else:
        print("Invalid option. Exiting...")
