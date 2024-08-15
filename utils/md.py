import re


def extract_contract_titles(md_file_path):
    # Read the Markdown file
    with open(md_file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # Split the content into sections
    sections = re.split(r'\n## ', md_content)

    # Find the "Contratos" section
    contratos_content = ""
    for section in sections:
        if section.startswith("Contratos"):
            contratos_content = section
            break

    if not contratos_content:
        return []

    # Extract contract titles
    contract_titles = re.findall(r'###\s*(\S+)', contratos_content)

    return contract_titles
