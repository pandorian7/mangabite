from mangasites import MangaSite
from mangabite.request import DestObj

tls = MangaSite.tools()


class MangaParkV2(MangaSite):
    netloc = ['v2.mangapark.net']
    _title_sel = ('div.path span.loc a')

    def recognize(self, dest_obj: DestObj):
        nav = dest_obj.soup.select_one('div.path')
        return tls.manga_page_kind(var=bool(nav), series=False, chapter=True)

    @MangaSite._chapter_required
    def titles(self, dest_obj: DestObj):
        series, chapter = dest_obj.soup.select_one(
            'div.path span.loc').contents[:2]
        series = tls.ele_text(series)
        chapter = chapter.replace('/', '').strip()
        return series, chapter

    @MangaSite._series_required
    def chapters(self, dest_obj: DestObj):
        versions = dest_obj.soup.select('div.stream')
        return len(versions)


mp = MangaParkV2()

url = 'https://v2.mangapark.net/manga/i-was-wrong-hakuri/i1306190/c1'
url_series = 'https://v2.mangapark.net/manga/i-was-wrong-hakuri'
url_series_1 = 'https://v2.mangapark.net/manga/on-a-leash-aji'

req = mp.Request(url_series_1)

res = mp.chapters(req)
print(res)
