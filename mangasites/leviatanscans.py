from mangabite.site import MangaSite
from mangabite.request import DestObj
from mangabite.naming import Manga


class Leviatanscans(MangaSite):
    netloc = ['en.leviatanscans.com']
    __title_selectors = 'ol.breadcrumb li'
    __chapters_selectors = ('li a', 'href')
    __chapter_images_selectors = ('div.reading-content img', 'src')

    def _validator(self, destObj: DestObj):
        return self.netloc == destObj.url_data.netloc

    def recognize(self, dest_obj: DestObj):
        heading = dest_obj.soup.select('div#manga-title')
        if len(heading) == 1:
            return Manga.Series
        else:
            return Manga.Chapter

    @MangaSite._chapter_required
    def titles(self, dest_obj: DestObj):
        lis = dest_obj.soup.select(self.__title_selectors)
        series_name = lis[-2].a.contents[0].strip()
        chapter_name = lis[-1].contents[0].strip()
        return series_name, chapter_name

    @MangaSite._series_required
    def chapters(self, dest_obj: DestObj):
        end = '' if dest_obj.url[-1] == '/' else '/'
        dest_obj = DestObj(dest_obj.url + end + 'ajax/chapters', method='POST')
        tag_sel, attr = self.__chapters_selectors
        return [link.get(attr) for link in dest_obj.soup.select(tag_sel)][::-1]

    @MangaSite._chapter_required
    def chapter_images(self, dest_obj: DestObj):
        tag_sel, attr = self.__chapter_images_selectors
        return [link.get(attr).strip() for link in dest_obj.soup.select(tag_sel)]
