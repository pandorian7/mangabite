from . import MangaSite
import re


class ReaperScans(MangaSite):
    use_cloudscrapper = True
    netloc = ['reaperscans.com']
    _title_sel = ('div.text-center p.font-semibold', 'nav.border-b div.hidden')
    _chapter_sel = ('div.pb-4 div div ul li a', 'href')
    _chapter_images_sel = ('main.mb-auto img', 'src')

    def recognize(self, dest_obj):
        # n_navs = len(dest_obj.soup.find_all('nav'))
        n_navs = len(dest_obj.url_data.parts)
        # return MangaSite.tools().manga_page_kind(var=n_navs, chapter=3, series=2)
        return MangaSite.tools().manga_page_kind(var=n_navs, chapter=4, series=2)

    def titles(self, dest_obj):
        return super()._titles(dest_obj)

    def chapters(self, dest_obj):
        return super()._chapters(dest_obj)

    def chapter_images(self, dest_obj):
        def clean_func(string): return re.search(
            '(?P<url>http.*)', string).group('url')
        return list(map(clean_func, super()._chapter_images(dest_obj)))
