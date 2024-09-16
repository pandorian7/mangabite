from mangabite.site import MangaSite
from mangabite.request import DestObj
from mangabite.naming import Manga

from urllib.parse import urlparse, urlunparse


class WebToons(MangaSite):
    netloc = 'www.webtoons.com'

    def _validator(self, destObj: DestObj):
        return self.netloc == destObj.url_data.netloc

    def recognize(self, dest_obj: DestObj):
        comment_area = dest_obj.soup.select_one('div.comment_area')
        if comment_area:
            return Manga.Chapter
        else:
            return Manga.Series

    @MangaSite._chapter_required
    def titles(self, dest_obj: DestObj):
        info_bar = dest_obj.soup.select_one('div.subj_info')
        series_name = info_bar.a['title']
        chapter_name = info_bar.h1['title']
        return series_name, chapter_name

    def __build_url(self, base, path):
        return urlunparse(urlparse(base)._replace(**{key: val for key, val in urlparse(path)._asdict().items() if val}))

    @MangaSite._series_required
    def get_series_pages(self, dest_obj: DestObj):
        page_anchors = dest_obj.soup.select('div.paginate a')
        links = map(lambda link: url if link == '#' else self.__build_url(
            url, link), [a['href'] for a in page_anchors])
        return list(links)[::-1]


webtoons = WebToons()

url = 'https://www.webtoons.com/en/romance/truebeauty/list?title_no=1436'

obj = DestObj(url, verbose=True)

vals = webtoons.get_series_pages(obj)
print(vals)
