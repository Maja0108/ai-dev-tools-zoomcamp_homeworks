import zipfile
import os
import requests

def download_and_extract_zip(url: str, extract_dir: str):
    """Download and extract the zip file."""
    zip_filename = url.split("/")[-1]
    if not os.path.exists(zip_filename):  # Avoid re-downloading
        response = requests.get(url)
        with open(zip_filename, 'wb') as f:
            f.write(response.content)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Filter for only .md and .mdx files
    md_files = []
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                md_files.append(os.path.join(root, file))
    return md_files

# Usage:
zip_url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
files = download_and_extract_zip(zip_url, "fastmcp-extracted")

from minsearch import minsearch
# Initialize search engine
search = minsearch.MinSearch()

def index_files(files: list):
    """Index content from files."""
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Modify file path
        filename = os.path.relpath(file, "fastmcp-main")
        search.add_document(content=content, filename=filename)

# Index the extracted .md and .mdx files
index_files(files)
