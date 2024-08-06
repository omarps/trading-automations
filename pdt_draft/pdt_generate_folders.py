import os

def create_folder_structure(base_path, date):
    # Define the folder structure
    folder_structure = ["graficos", "contratos", "gammas"]

    # Join base_path and date to create the base directory
    full_path = os.path.join(base_path, date)

    # Create the base directory if it does not exist
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    # Create the folder structure
    for folder in folder_structure:
        folder_path = os.path.join(full_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Add a summary file to the folder
    # with name format SPY_{date}_summary.md
    # based on the summary.sample.md file
    summary_file = os.path.join(full_path, f"SPY_{date}_summary.md")
    if not os.path.exists(summary_file):
        with open("../summary.sample.md", "r") as f:
            content = f.read()
            content = content.replace("{{date}}", date)
            with open(summary_file, "w") as f:
                f.write(content)

    print(f"Folder structure created at: {full_path}")

if __name__ == "__main__":
    base_path = "/Users/omarps/Library/CloudStorage/OneDrive-Personal/Proyectos/CDI/PDT/2024/2024q3"  # Replace with the path to your base folder
    date = "20240718"  # Replace with the date
    create_folder_structure(base_path, date)
