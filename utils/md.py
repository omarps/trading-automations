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

def extract_contract_contents(md_file_path):
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
    contract_titles = [title.lstrip('.') for title in re.findall(r'###\s*(\S+)', contratos_content)]

    # Split by contract titles
    contract_bodies = re.split(r'###\s*\S+', contratos_content)
    contract_bodies.pop(0)

    # Strip leading and trailing newlines from contract bodies
    contract_bodies = [body.strip() for body in contract_bodies]
    contract_bodies = [body.replace("\n\n", "<br/>") for body in contract_bodies]

    # Return a dictionary with the contract titles as keys
    # and the contract contents as values
    # contract_contents = dict(zip(contract_titles, contract_contents[1:]))
    contract_contents = dict(zip(contract_titles, contract_bodies))

    return contract_contents
