import requests
from bs4 import BeautifulSoup

from requests_html import HTMLSession


class catch_data:

    def __init__(self, url: str) -> None:
        self.url = url
        pass

    def proceed(self):

    # Создаем сессию
        session = HTMLSession()

        response = session.get(self.url)

        response.html.render()

        soup = BeautifulSoup(response.html.html, "html.parser")

        target_h3 = soup.find("h3", string=lambda text: text and "₽" in text)

        
        if target_h3:
            return float(target_h3.get_text(strip=True))
        else:
            return 'I cant parse this'
        
    