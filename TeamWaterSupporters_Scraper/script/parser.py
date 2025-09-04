"""
parser.py

Module to parse supporter data from HTML content.
"""
print("[INFO] --- Installing 'PARSER' libraries...")

from bs4 import BeautifulSoup



# -----------------------------
# Configuration
# -----------------------------

# -----------------------------
# Parsing functions
# -----------------------------
def parse_supporter_block(html_block) -> dict:
    """
    Parse a single supporter block to extract data.
    Returns a dictionary with keys: name, amount, date, location, messaged
    """

    def safe_get_text(block, tag, class_name, default=""):
        """Safely extract text from a tag with a given class name."""
        el = block.find(tag, class_=class_name)
        # return el.text.strip() if el else default
        return el.text if el else default

    def safe_get_html(block, tag, class_name, default=""):
        """Safely extract innerHTML instead of just text."""
        el = block.find(tag, class_=class_name)
        return el.decode_contents().strip() if el else default

    # Example structure
    return {
        "name": safe_get_text(html_block, "div", "wrap-anywhere line-clamp-3 font-[Sora] text-base font-bold leading-[20px] sm:text-lg"),
        "amount": safe_get_text(html_block, "div", "bg-(--navy-blue) rounded-sm px-1.5 py-1 font-[Sora] text-base font-bold text-white sm:text-xl"),
        "date": safe_get_text(html_block, "div", "font-[Sora] text-[10px] font-bold"),
        "location": safe_get_text(html_block, "div", "name"),
        "message": safe_get_text(html_block, "div", "wrap-anywhere font-[Sora] text-xs")
    }


def parse_page(html_content: str, page_no: int) -> list:
    """Parse all supporter entries from a single HTML page."""
    supporters = []
    soup = BeautifulSoup(html_content, "html.parser")

    # Example selector (adjust to real page structure)
    blocks = soup.find_all("div", class_="white-box")[1:]
    print(f"[DEBUG] --- Found {len(blocks)} supporters in page {page_no}")
    for block in blocks:
        supporter = parse_supporter_block(block)
        supporters.append(supporter)
    return supporters


def parse_multiple_pages(list_of_html: list) -> list:
    """Parse multiple pages and combine supporter data."""

    all_supporters = []
    for index, html in enumerate(list_of_html, start=1):
        all_supporters.extend(parse_page(html, index))
    return all_supporters
