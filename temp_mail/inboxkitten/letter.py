import re
import requests
from ..mail import letter


class Letter(letter.Letter):
    def __init__(self, url, headers, timestamp, proxies):
        super().__init__(headers['to'], headers['from'], headers['subject'], timestamp, proxies)
        self.__letter_id = '-'.join(re.findall(r'https://(.*)\.api\.mailgun\.net/v3/domains/inboxkitten\.com/messages/(.*)', url)[0])

    @property
    def letter(self):
        if self._latter:
            return self._latter
        r = requests.get(f'https://inboxkitten.com/api/v1/mail/getHtml?mailKey={self.__letter_id}', proxies=self._proxies)
        if r.status_code == 200:
            self._latter = re.sub(r'<script[^>]*>([\s\S]*?)</script>', '', r.text)
            return self._latter
