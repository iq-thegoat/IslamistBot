import datetime
from loguru import logger
from bs4 import BeautifulSoup
from dorrar.Types import Hadith
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import quote
from bs4 import element
import re
import colorama
from typing import Optional
from icecream import ic


def check_item(item):
    try:
        if item:
            return item
    except:
        return None


def extract_urls_from_text(text):
    # Define a regular expression pattern for URLs
    url_pattern = re.compile(r"https?://\S+")

    # Find all matches in the text
    urls = re.findall(url_pattern, text)

    return urls


def remove_html_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text


class Parser:
    """
    This class provides methods for parsing book information and performing book searches.
    """

    def __init__(self):
        """
        Constructor for the Parser class.
        """
        return None  # Constructor with no actual code

    def __by_id_inner(self, id: str, soup: BeautifulSoup) -> Optional[str]:
        """
        Private method to extract content by element ID from a BeautifulSoup object.

        Args:
            id (str): The ID of the HTML element to find.
            soup (BeautifulSoup): The BeautifulSoup object to search in.

        Returns:
            str | None: The content of the element if found, or None if not found.
        """
        element = soup.find(id=id)
        if element:
            element = element.encode_contents().decode()
        return element

    def __by_id(self, id: str, soup: BeautifulSoup):
        """
        Private method to find an element by ID in a BeautifulSoup object.

        Args:
            id (str): The ID of the HTML element to find.
            soup (BeautifulSoup): The BeautifulSoup object to search in.

        Returns:
            element: The BeautifulSoup element if found, or None if not found.
        """
        element = soup.find(id=id)
        return element

    def parse_hadith_page(self, HTML) -> Hadith:
        """
        Parse a book page given its URL and return a Hadith object.

        Args:
            url (str): The URL of the book page to parse.

        Returns:
            Hadith: A Hadith object containing information about the parsed book.
        """
        soup = BeautifulSoup(str(HTML), "html.parser")
        text = soup.find("h5", {"class": "h5-responsive"})

        # Extract the book title if found
        if text:
            text = (
                text.encode_contents()
                .decode()
                .replace('<span class="search-keys">', "REDALERTRIGHT")
                .replace("</span>", "REDALERTLEFT")
            )
            text = text.strip().replace("\t", " ")

        infoblock = soup.find("div", {"class": "d-block mb-2"})

        narrator = None
        muhadith = None
        source = None
        page = None
        ruling = None
        url = None
        sharh = None
        if infoblock:
            data = infoblock.find_all("strong")
            a_tag = soup.find("a", class_="btn")
            if a_tag:
                url = extract_urls_from_text(str(a_tag))
                if url[0]:
                    url = url[0]
            tafsir = infoblock.find(
                "a", {"class": "xplain default-text-color px-2", "data-toggle": "modal"}
            )
            if tafsir:
                sharh = tafsir["xplain"]
                if sharh:
                    sharh = "https://dorar.net/hadith/sharh/" + sharh
            for block in data:
                if "الراوي" in block.text:
                    narrator = block.text
                    if narrator:
                        narrator = narrator.split(":")[1].strip().replace("\t", " ")
                    else:
                        narrator = None
                elif "| المحدث :" in block.text:
                    muhadith = block.text.strip()
                    if muhadith:
                        muhadith = muhadith.split(":")[1].strip().replace("\t", " ")

                elif "المصدر" in block.text:
                    source = block.text
                    if source:
                        source = source.split(":")[1].strip().replace("\t", " ")

                elif "الصفحة أو الرقم" in block.text:
                    page = block.text
                    if page:
                        page = page.split(":")[1].strip().replace("\t", " ")
                elif "خلاصة حكم المحدث" in block.text:
                    ruling = block.text
                    if ruling:
                        ruling = ruling.split(":")[1].strip().replace("\t", " ")

        text = remove_html_tags(text)
        HADITH = Hadith(
            text=text,
            narrator=narrator,
            muhadith=muhadith,
            ruling=ruling,
            source=source,
            url=url,
            page=page,
            sharh=sharh,
        )
        return HADITH

    def search(self, query, specialist=False, limit: int = 2) -> Hadith:
        """
        Search for books using a query and return a list of SearchResult objects.

        Args:
            query (str): The search query to find books.

        Returns:
            list[Hadith]: A list of Hadith objects.
        """
        limit = limit * 2
        session = HTMLSession()
        query = quote(query)
        if specialist:
            URL = f"https://dorar.net/hadith/search?q={query.strip()}&st=w&xclude=&rawi%5B%5D=#specialist"
        else:
            URL = f"https://dorar.net/hadith/search?q={query.strip()}&st=w&xclude=&rawi%5B%5D=#home"

        r = session.get(URL)
        # Retry the request up to 10 times if it doesn't return a 200 status code
        for i in range(10):
            if r.status_code != 200:
                r = session.get(URL)
            else:
                break

        soup = BeautifulSoup(r.content, "html.parser")
        ahadith = soup.find_all("div", {"class": "border-bottom py-4"})
        unique_hadiths = set()
        for n, hadith in enumerate(ahadith):
            current_hadith = self.parse_hadith_page(hadith)
            unique_hadiths.add(current_hadith)
            if n >= limit:
                break
        unique_hadiths = list(unique_hadiths)
        for hadith in unique_hadiths:
            for second_hadth in unique_hadiths:
                if hadith == second_hadth:
                    unique_hadiths.pop(unique_hadiths.index(hadith))
        return unique_hadiths
