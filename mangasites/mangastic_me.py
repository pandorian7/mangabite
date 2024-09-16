from mangabite.site import MangaSite
from mangabite.request import DestObj
from mangabite.naming import Manga
from itertools import chain
from bs4 import element


class MangaStic(MangaSite):
    netloc = ['mangastic.net']
    __breadcrumb_selector = 'ol.breadcrumb li'
    __chapters_selectors = ('ul.version-chap li a', 'href')
    __chapter_images_selectors = ('div.reading-content div img', 'data-src')

    # def _validator(self, destObj: DestObj):
    #     return self.netloc == destObj.url_data.netloc

    def breadcrumb(self, destObj: DestObj):
        tags = destObj.soup.select(self.__breadcrumb_selector)
        contents = map(lambda tag: tag.contents, tags)
        contents = chain(*contents)
        contents = filter(lambda e: e != '\n', contents)
        return list(contents)

    def recognize(self, dest_obj: DestObj):
        breadcrumb = self.breadcrumb(dest_obj)
        if type(breadcrumb[-1]) == element.Tag:
            return Manga.Series
        else:
            return Manga.Chapter

    @MangaSite._chapter_required
    def titles(self, dest_obj: DestObj):
        breadcrump = self.breadcrumb(dest_obj)
        series_name = breadcrump[-2].contents[0].strip()
        chapter_name = breadcrump[-1].strip()
        return series_name, chapter_name

    @MangaSite._series_required
    def chapters(self, dest_obj: DestObj):
        tag_sel, attr = self.__chapters_selectors
        return [link.get(attr) for link in dest_obj.soup.select(tag_sel)][::-1]

    @MangaSite._chapter_required
    def chapter_images(self, dest_obj: DestObj):
        tag_sel, attr = self.__chapter_images_selectors
        return [link.get(attr).strip() for link in dest_obj.soup.select(tag_sel)]

# to be continued
