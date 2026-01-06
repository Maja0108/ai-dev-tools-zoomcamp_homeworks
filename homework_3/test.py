import requests

def fetch_page_content(url):
    # Prepend the URL with r.jina.ai
    formatted_url = f"https://r.jina.ai/{url}"
    
    # Send a request to fetch the content
    response = requests.get(formatted_url)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch the content. Status code: {response.status_code}"

def calculate_character_count(content):
    # Calculate the number of characters in the content
    return len(content)

if __name__ == "__main__":
    # Test URL
    test_url = "https://github.com/alexeygrigorev/minsearch"  # Example URL; replace with any URL you want
    
    # Fetch page content
    content = fetch_page_content(test_url)
    
    if not content.startswith("Error"):
        # Calculate the character count of the content
        character_count = calculate_character_count(content)
        print(f"Character count of the content: {character_count}")
        
        # Save the content to a markdown file
        with open("page_content.md", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("Page content saved as page_content.md")
    else:
        print(content)
