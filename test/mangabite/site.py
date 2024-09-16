from .request import DestObj
from .naming import Manga


class MangaSiteTools:
    @staticmethod
    def manga_page_kind(var, series, chapter):
        if var == series:
            return Manga.Series
        elif var == chapter:
            return Manga.Chapter
        else:
            raise Exception(f'saw "{var}" insted of "{series}" or "{chapter}"')

    @staticmethod
    def ele_text(ele):
        return ele.contents[0].strip()

    @staticmethod
    def parse_html_list(soup, xpath, attr=None, reverse=False):
        eles = soup.select(xpath)
        if attr:
            eles = [ele[attr].strip() for ele in eles]
        if reverse:
            eles.reverse()
        return eles


class MangaSite:
    netloc = None
    use_cloudscrapper = False
    _title_sel = ('', '')
    _chapter_sel = ('', '')
    _chapter_images_sel = ('', '')

    def _validator(self, destObj: DestObj):
        return destObj.url_data.netloc == self.netloc or destObj.url_data.netloc in self.netloc

    def Request(self, *args,  **kwargs):
        return DestObj(*args, **kwargs, name=self.netloc, use_cloudscrapper=self.use_cloudscrapper, validator=self._validator)

    def _chapter_required(func):
        def decorator(self, dest_obj: DestObj):
            if not self.recognize(dest_obj) == Manga.Chapter:
                raise Exception('chapter element required')
            return func(self, dest_obj)
        return decorator

    def _series_required(func):
        def decorator(self, dest_obj: DestObj):
            if not self.recognize(dest_obj) == Manga.Series:
                raise Exception('series element required')
            return func(self, dest_obj)
        return decorator

    def recognize(self, dest_obj: DestObj):
        raise NotImplementedError

    def titles(self, dest_obj: DestObj):
        raise NotImplementedError

    @_chapter_required
    def _titles(self, dest_obj: DestObj):
        series_sel, chapter_sel = self._title_sel
        series_name = MangaSiteTools.ele_text(
            dest_obj.soup.select_one(series_sel))
        chapter_name = MangaSiteTools.ele_text(
            dest_obj.soup.select_one(chapter_sel))
        return series_name, chapter_name

    def chapters(self, dest_obj: DestObj):
        raise NotImplementedError

    @_series_required
    def _chapters(self, dest_obj: DestObj):
        xpath, attr = self._chapter_sel
        return MangaSiteTools.parse_html_list(dest_obj.soup, xpath, attr, reverse=True)

    def chapter_images(self, dest_obj: DestObj):
        raise NotImplementedError

    @_chapter_required
    def _chapter_images(self, dest_obj: DestObj):
        xpath, attr = self._chapter_images_sel
        return MangaSiteTools.parse_html_list(dest_obj.soup, xpath, attr)

    @staticmethod
    def tools():
        return MangaSiteTools
