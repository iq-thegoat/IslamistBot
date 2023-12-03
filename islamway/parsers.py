import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import datetime
from islamway.Types import Nasheed
import re


def htmlit(data):
    with open("data.html","w",errors="ignore") as f:
        f.write(data)

class Parser:
    class _Helpers:

        @staticmethod
        def _by_id_inner(id: str, soup: BeautifulSoup) -> str | None:
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

        @staticmethod
        def make_valid_filename(s):
            # Remove illegal characters
            s = re.sub(r'[\/:*?"<>|]', '', s)

            # Replace spaces with underscores
            s = s.replace(' ', '_')
            s = s.replace("؟","-")

            # Limit the length (adjust as needed)
            s = s[:255]

            return s

        @staticmethod
        def _ina(element)-> tuple:
            try:
                a_tag = element.find("a")
                if a_tag:
                    url = a_tag.get("href")
                    if url:
                        url = f"https://ar.islamway.net{url}"
                    else:
                        url = None

                    inner = a_tag.text.strip()
                    if not inner:
                        inner = None

                else:
                    url = None
                    inner = None
                return (url,inner)
            except:
                return (None,None)


    class Anasheed:
        @staticmethod
        def _nasheed_parser(soup) -> Nasheed:



            name = soup.find("h2",{"class":"nasheed-title"})
            nasheed_url,nasheed_name = Parser._Helpers._ina(name)
            publisher = soup.find("h3",{"class":"media-heading user-name"})
            publisher_url,publisher_name = Parser._Helpers._ina(publisher)
            try:
                publisher_img = soup.find("img",{"class":"media-object avatar veiled"})
                publisher_img = publisher_img.get("data-src")
                if publisher_img:
                    publisher_img = str("https:"+publisher_img)
            except:
                publisher_img = None
            try:
                views = soup.find("span",{"class","views-count"}).text.strip()
                views = int(views.replace(',', ''))
            except:
                views = None

            try:
                likes = soup.find("span",{"class":"up-votes"}).text.strip()
                likes = int(likes.replace(",", ""))
            except:
                likes = None

            try:
                dislikes = soup.find("span",{"class":"down-votes"}).text.strip()
                dislikes = int(str(dislikes).replace(",", ""))
            except:
                dislikes = None

            r = requests.get(nasheed_url)
            soup = BeautifulSoup(r.content,"html.parser")
            try:
                text = Parser._Helpers._by_id_inner(id="entry-summary",soup=soup)
            except:
                text = None

            try:
                time = soup.find("span",{"class":"darker"}).text.strip()
                if time:
                    try:
                        time = datetime.datetime.strptime(time,"%Y-%m-%d")
                    except Exception as e:
                        print(e)
                else:
                    time = None
            except:
                time = None
            htmlit(r.text)
            try:
                download_div = soup.find("div",{"class","iw-resources"})
                div_tag = download_div.find("a",download=True)
                download_link = div_tag.get("href")
                filename = div_tag.get("download")
                if filename:
                    filename = Parser._Helpers.make_valid_filename(filename)
            except:
                download_link = None
                filename = None
            nasheed = Nasheed(name=nasheed_name,filename=filename,publisher=publisher_name,publisher_img=publisher_img,publisher_profile=publisher_url,publish_date=time,views=views,likes=likes,dislikes=dislikes,nasheed_url=nasheed_url,download_url=download_link,text=text)
            return  nasheed

        @staticmethod
        def _proccess_nasheed_url(url:str,limit:int=5):
            nasheeds = []
            res = requests.get(url)
            soup = BeautifulSoup(res.content,"html.parser")
            anasheed = soup.find_all("div",{"class":"iw-panel"})
            for count,nasheed in enumerate(anasheed,start=0):
                if count == limit:
                    break
                try:
                    nasheeds.append(Parser.Anasheed._nasheed_parser(nasheed))
                except:
                    pass
            return nasheeds

        @staticmethod
        def search_nasheed(query:str,limit:int=5) -> list[Nasheed]:
            nasheeds = []
            query = quote(query)
            url = f"https://ar.islamway.net/anasheed?q={query}&type=nasheed"
            ret = Parser.Anasheed._proccess_nasheed_url(url,limit)
            return ret

        @staticmethod
        def most_popular(limit:int=5):
            url = "https://ar.islamway.net/anasheed?view=popular"
            ret = Parser.Anasheed._proccess_nasheed_url(url,limit)
            return ret

        @staticmethod
        def most_recent (limit:int=5):
            url = "https://ar.islamway.net/anasheed?view=new"
            ret = Parser.Anasheed._proccess_nasheed_url(url,limit)
            return ret

        @staticmethod
        def most_viewed(limit:int=5):
            url = "https://ar.islamway.net/anasheed?view=visits"
            ret = Parser.Anasheed._proccess_nasheed_url(url,limit)
            return ret


        @staticmethod
        def highest_rated(limit:int=5):
            url = "https://ar.islamway.net/anasheed?view=rates"
            ret = Parser.Anasheed._proccess_nasheed_url(url,limit)
            return ret

    class Fatawa:

        @staticmethod
        def search_fatwa(query:str,limit:int=5):
            nasheeds = []
            query = quote(query)
            url = f"https://ar.islamway.net/fatawa?q={query}&type=fatwa"
            r = Parser.Fatawa._proccess_fatwa_url(url)
            return  r

        @staticmethod
        def _proccess_fatwa_url(url:str,limit:int=5):
            fatwas = []
            res = requests.get(url)
            soup = BeautifulSoup(res.content,"html.parser")
            anasheed = soup.find_all("div",{"class":"iw-panel"})
            for count,fatwa in enumerate(anasheed,start=0):
                if count == limit:
                    break
                try:
                    fatwas.append(Parser.Fatawa.fatwa_parser(fatwa))
                except:
                    pass
            return fatwas

        @staticmethod
        def fatwa_parser():
            ...

    class Books:

        @staticmethod
        def search_book(query:str,limit:int=5):
            query = quote(query)
            url   = f"https://ar.islamway.net/books?q={query}&type=book"
            r     = Parser.Books._proccess_book_url(url)
            return  r

        @staticmethod
        def _proccess_book_url(url,limit:int):
            books = []
            res = requests.get(url)
            soup = BeautifulSoup(res.content,"html.parser")
            anasheed = soup.find_all("div",{"class":"iw-panel"})
            for count,book in enumerate(anasheed,start=0):
                if count == limit:
                    break
                try:
                    books.append(Parser.Books._book_parser(book))
                except:
                    pass
            return books

        @staticmethod
        def _book_parser(soup):
            ...


