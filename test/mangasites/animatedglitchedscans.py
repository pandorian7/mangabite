from mangabite.site import MangaSite
from mangabite.naming import Manga
from mangabite.request import DestObj
import re
import json
from .asura_gg import Asura


class AnimatedGlitchedScans1(Asura):
    netloc = 'anigliscans.com'
    __chapter_images_selectors = ('div#readerarea img', 'src')

    def titles(self, dest_obj: DestObj):
        series_title, chapter_title = super().titles(dest_obj)
        if chapter_title[0] in ['-', '–']:
            chapter_title = chapter_title[1:].strip()
        return series_title, chapter_title


class AnimatedGlitchedScans(MangaSite):
    netloc = ['anigliscans.com']
    __title_selectors = ('h1.entry-title', 'div.allc a')
    __chapters_selectors = ('div#chapterlist ul li a', 'href')

    def _validator(self, destObj: DestObj):
        return self.netloc == destObj.url_data.netloc

    def recognize(self, dest_obj: DestObj):
        info_box = dest_obj.soup.select_one('div.infox')
        if info_box:
            return Manga.Series
        else:
            return Manga.Chapter

    @MangaSite._chapter_required
    def titles(self, dest_obj: DestObj):
        soup = dest_obj.soup
        full_name_sel, series_name_sel = self.__title_selectors
        full_name = soup.select_one(full_name_sel).contents[0].strip()
        series_title = soup.select_one(series_name_sel).contents[0].strip()
        chapter_title = full_name[len(series_title):].strip()
        if chapter_title[0] in ['-', '–']:
            chapter_title = chapter_title[1:].strip()
        return series_title, chapter_title

    @MangaSite._series_required
    def chapters(self, dest_obj: DestObj):
        tag_sel, attr = self.__chapters_selectors
        return [link.get(attr) for link in dest_obj.soup.select(tag_sel)][::-1]

    @MangaSite._chapter_required
    def chapter_images(self, dest_obj: DestObj):
        scripts = dest_obj.soup.select('script')
        data_script = filter(
            lambda scr: 'ts_reader.run' in ''.join(scr.contents), scripts)
        data_script = list(data_script)[0]
        json_str = re.match(r'ts_reader\.run\((?P<dict>.*)\);',
                            data_script.contents[0]).group('dict')
        dic = json.loads(json_str)
        images = dic['sources'][0]['images']
        return images
