from mangasites import MangaSite

tls = MangaSite.tools()


class MangaBTT(MangaSite):
    netloc = ['mangabtt.com']
    _chapter_sel = ('div.list-chapter ul li div a', 'href')
    _chapter_images_sel = ('div.reading-detail div img', 'data-src')

    def recognize(self, dest_obj):
        navs = dest_obj.soup.select('ul.breadcrumb li')
        return tls.manga_page_kind(var=len(navs), series=2, chapter=3)

    @MangaSite._chapter_required
    def titles(self, dest_obj):
        _, series, chapter = dest_obj.soup.select('ul.breadcrumb li')
        series_name = tls.ele_text(series.find('span'))
        chapter_name = tls.ele_text(chapter.find('span'))
        return series_name, chapter_name

    @MangaSite._series_required
    def chapters(self, dest_obj):
        storyID = dest_obj.soup.select_one('input#storyID')['value']
        req = self.Request(url="https://mangabtt.com/Story/ListChapterByStoryID", method="POST",
                           data='{"StoryID":"'+storyID+'"}', headers={"Content-Type": "application/json"})
        return tls.parse_html_list(req.soup, 'li div.chapter a', 'href', reverse=True)

    def chapter_images(self, dest_obj):
        return super()._chapter_images(dest_obj)


url_series = 'https://mangabtt.com/manga/death-god-29463'
url_series_1 = 'https://mangabtt.com/manga/astral-pet-store-19302'
url_chapter = 'https://mangabtt.com/manga/death-god/chapter-0-eng-li/258385'
url_chapter_1 = 'https://mangabtt.com/manga/astral-pet-store/chapter-39-eng-li/385430'

mbtt = MangaBTT()
req = mbtt.Request(url=url_chapter)
res = mbtt.chapter_images(req)
print(res)
