"""
parser.py

Module to parse supporter data from HTML content.
"""

from bs4 import BeautifulSoup

# -----------------------------
# Parsing functions
# -----------------------------
def parse_supporter_block(html_block) -> dict:
    """
    Parse a single supporter block to extract data.
    Returns a dictionary with keys: name, amount, date, location, message
    """
    # Example structure
    return {
        "name": html_block.find("div", class_="wrap-anywhere line-clamp-3 font-[Sora] text-base font-bold leading-[20px] sm:text-lg"),
        "amount": html_block.find("div", class_="bg-(--navy-blue) rounded-sm px-1.5 py-1 font-[Sora] text-base font-bold text-white sm:text-xl"),
        "date": html_block.find("div", class_="font-[Sora] text-[10px] font-bold"),
        "location": html_block.find("p", class_="name"),
        "message": html_block.find("div", class_="wrap-anywhere font-[Sora] text-xs"),
    }


def parse_page(html_content: str) -> list:
    """Parse all supporter entries from a single HTML page."""
    # soup = BeautifulSoup(html_content, "lxml")
    soup = BeautifulSoup(html_content, "html.parser")
    supporters = []

    # Example selector (adjust to real page structure)
    # blocks = soup.select(".supporter-block")
    # blocks = soup.select(".min-h-160.flex.flex-col.gap-4")
    blocks = soup.find_all("div", class_="white-box")[1:]
    print('blocks', len(blocks))
    for block in blocks:
        supporter = parse_supporter_block(block)
        supporters.append(supporter)
    return supporters


def parse_multiple_pages(list_of_html: list) -> list:
    """Parse multiple pages and combine supporter data."""
    all_supporters = []
    for html in list_of_html:
        page_supporters = parse_page(html)
        all_supporters.extend(page_supporters)
    return all_supporters
