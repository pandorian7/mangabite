from requests.exceptions import InvalidURL, RequestException
from collections import namedtuple
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


class DestObj:

    __URLData = namedtuple('URLData', ['netloc', 'slag', 'parts'])

    def __error_on_none(func):
        def decorator(self, *args, **kwargs):
            tmp = self.error_on_none
            self.error_on_none = True
            data = func(self, *args, **kwargs)
            self.error_on_none = tmp
            return data

        return decorator

    def __get_data(self, key, required=False):
        data = self.__data.get(key, None)
        if (self.error_on_none) and (not data) and (not required):
            raise KeyError(f"{key} is not found")
        return data

    def __init__(self, url=None, res=None, soup=None, name=None, error_on_none=False, method='GET', retries=1, use_cloudscrapper=False, verbose=False, validator=None, headers={}, **kwargs):
        self.__data = {'url': url, 'res': res, 'soup': soup, 'method': method}
        self.error_on_none = error_on_none
        self.use_cloudscrapper = use_cloudscrapper
        self.name = name
        self.retries = retries
        self.verbose = verbose
        self.validator = validator
        self.headers = headers
        self.kwargs = kwargs

    def __scrapper(self):
        scrapper = self.__data.get('scrapper', None)
        if not scrapper:
            import cloudscraper
            scrapper = cloudscraper.create_scraper()
            self.__data['scrapper'] = scrapper
        return scrapper

    def __http_handler(self):
        if self.use_cloudscrapper:
            return self.__scrapper()
        else:
            return requests

    def __make_request(self):
        handler = self.__http_handler()
        url = self.__get_data('url')
        if self.validator:
            if not self.validator(self):
                raise InvalidURL(
                    f'this url({url}) is not compatible with {self.name}')
        res = None
        for r in range(self.retries):
            try:

                if self.validator:
                    if not self.validator(self):
                        raise InvalidURL(
                            f'this url({url}) is not compatible with {self}')
                print('requesting')
                res = handler.request(self.__get_data(
                    'method'), url, headers=self.headers, **self.kwargs)

                if not res.ok:
                    raise RequestException(
                        f'request to {self.url} failed with error code {res.status_code}')
                break

            except Exception as err:
                print(f'try {r+1}: {err}')
        if not res:
            raise Exception(
                f'exceeded maximum number of requests({self.retries})')
        return res

    @property
    def url(self):
        data = self.__get_data('url')
        return data

    @property
    def response(self):
        data = self.__data
        res = data.get('res', None)
        if not res:
            if self.verbose:
                print(f'receving from {self.url}')
            res = self.__make_request().content
            data['res'] = res
        return res

    @property
    def soup(self):
        data = self.__data
        soup = data.get('soup', None)
        if not soup:
            soup = BeautifulSoup(self.response, 'html.parser')
            data['soup'] = soup
        return soup

    @property
    def settings(self):
        return {'error_on_none': self.error_on_none,
                'error_on_none': self.use_cloudscrapper,
                'name': self.name,
                'retries': self.retries,
                'verbose': self.verbose,
                'validator': self.validator,
                'headers': self.headers}

    def clear(self):
        self.__data.update({'res': None, 'soup':None})

    @property
    @__error_on_none
    def url_data(self):
        url_parsed = urlparse(self.url)
        parts = [pt for pt in url_parsed.path.split('/') if pt]
        return self.__URLData(url_parsed.netloc, url_parsed.path, parts)

    @classmethod
    def for_image(cls, url, use_cloudscrapper=False, retries=10):
        return cls(url, use_cloudscrapper=use_cloudscrapper, retries=retries, verbose=True)
