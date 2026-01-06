from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def count_data_occurrences(url: str) -> int:
    """Count occurrences of 'data' on a web page"""
    content = fetch_page_content(url)
    return content.lower().count('data')

if __name__ == "__main__":
    mcp.run()