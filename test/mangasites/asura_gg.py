from mangabite.errorHandler import retryWithRefreshOnError
from mangabite.site import MangaSite
from mangabite.request import DestObj
import re

tls = MangaSite.tools()


class Asura(MangaSite):
    use_cloudscrapper = True
    netloc = ['asura.gg', 'www.asurascans.com', 'asuratoon.com']
    _title_sel = ('h1.entry-title', 'div.allc a')
    _chapter_sel = ('div#chapterlist ul li a', 'href')
    _chapter_images_sel = ('div#readerarea p img', 'src')

    def recognize(self, dest_obj: DestObj):
        def is_series(dest_obj): return dest_obj.url_data.parts[0] == 'manga'
        return tls.manga_page_kind(var=is_series(dest_obj), chapter=False, series=True)

    @MangaSite._chapter_required
    def titles(self, dest_obj: DestObj):
        soup = dest_obj.soup
        full_name_sel, series_name_sel = self._title_sel
        full_name = tls.ele_text(soup.select_one(full_name_sel))
        series_name = tls.ele_text(soup.select_one(series_name_sel))
        chapter_name = full_name[len(series_name):].strip()
        return series_name, chapter_name

    def chapters(self, dest_obj: DestObj):
        return super()._chapters(dest_obj)

    def chapter_images(self, dest_obj):
        def clean_func(string): return re.search(
            '(?P<url>http.*)', string).group('url')
        res = retryWithRefreshOnError(super()._chapter_images, args=[dest_obj],cleanFunc=dest_obj.clear)
        return list(map(clean_func, res))


# class AsuraScans(Asura):
#     netloc = 'asurascans.com'

# class WWWAsuraScans(Asura):
#     use_cloudscrapper = True
#     netloc = 'www.asurascans.com'
