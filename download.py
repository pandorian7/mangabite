from mangabite.request import DestObj
from mangabite.site import MangaSite
from mangabite.naming import Manga
from mangasites import SiteHandler
from pathlib import Path
from time import sleep
from PIL import Image
import argparse
import io

ignore_images = []
start_from = None
stop_at = None
chapter_delay = None


def save_pdf(pdf_path, image_urls):
    interupted = False
    print(f'downloading {len(image_urls)} images')
    link_objs = [DestObj.for_image(url=url) for url in image_urls]
    images = [Image.open(io.BytesIO(obj.response)) for obj in link_objs]
    RGB_images = [img.convert('RGB') for img in images]
    try:
        RGB_images[0].save(pdf_path, save_all=True,
                           append_images=RGB_images[1:])
        return True
    except KeyboardInterrupt:
        interupted = True
    if interupted:
        return False
        raise KeyboardInterrupt('raised deled interuption')


def cleanFilename(sourcestring,  removestring="%:/,.\\[]<>*?"):
    # remove the undesireable characters
    return ''.join([c for c in sourcestring if c not in removestring])


def download_chapter(obj, site: MangaSite, save_location=Path('./manga')):
    global ignore_images
    chapter_images = [image for image in site.chapter_images(
        obj) if image not in ignore_images]
    series_name, chapter_name = site.titles(obj)
    series_name = cleanFilename(series_name)
    chapter_name = cleanFilename(chapter_name)
    pdf_dir: Path = save_location / series_name
    pdf_name = f'{series_name} - {chapter_name}.pdf'
    print(f'creating {pdf_name}')
    pdf_path = pdf_dir / pdf_name
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if not (pdf_path.exists() or (pdf_dir / 'read' / pdf_name).exists()):
        return save_pdf(pdf_path, chapter_images)
    else:
        print(f'{pdf_path} exists')
        return False


def handle_url(url, handler=None):
    global start_from, stop_at
    if not handler:
        handler = SiteHandler()
    site:MangaSite = handler.get_site(url)
    assert site
    obj = site.Request(url, error_on_none=True, verbose=True)
    if not site:
        raise Exception('site not available')
    match site.recognize(obj):
        case Manga.Chapter:
            return download_chapter(obj, site)
        case Manga.Series:
            chapters = site.chapters(obj)
            if start_from:
                chapters = chapters[chapters.index(start_from):]
            if stop_at:
                chapters = chapters[:chapters.index(stop_at)+1]
            for chapter in chapters:
                print(chapter)
                download_successful = handle_url(chapter)
                if chapter_delay and download_successful:
                    print(f'waiting {chapter_delay} seconds')
                    sleep(chapter_delay)


def main(args=None, handler=None):
    global ignore_images
    global start_from
    global stop_at
    global chapter_delay
    parser = argparse.ArgumentParser(prog='download manga')
    parser.add_argument('url')
    parser.add_argument('--ignore-images', nargs='*', default=[])
    parser.add_argument('--start-from')
    parser.add_argument('--stop-at')
    parser.add_argument('--chapter-delay', default=0, type=int)
    data = parser.parse_args(args)
    ignore_images += data.ignore_images
    start_from = data.start_from
    stop_at = data.stop_at
    chapter_delay = data.chapter_delay
    handle_url(data.url, handler=handler)


if __name__ == '__main__':
    main()
