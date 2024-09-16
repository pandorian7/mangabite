from mangabite.site import MangaSite
from urllib.parse import urlparse

from .toon69 import Toon69
from .asura_gg import Asura
from .mangabtt import MangaBTT
from .mangastic_me import MangaStic
from .reaperscans import ReaperScans
from .leviatanscans import Leviatanscans
from .animatedglitchedscans import AnimatedGlitchedScans

Sites = [Asura, MangaStic, Toon69, Leviatanscans,
         AnimatedGlitchedScans, ReaperScans, MangaBTT]


class SiteHandler:
    def __init__(self, custom_handlers=[]):
        self.__custom_handlers = custom_handlers

    @property
    def sites(self):
        return Sites + self.__custom_handlers

    @property
    def site_dic(self):
        site_objs = [site() for site in self.sites]
        return {netloc: site for site in site_objs for netloc in site.netloc}

    def get_site(self, url) -> MangaSite | None:
        return self.site_dic.get(urlparse(url).netloc)

    def add_custom_handler(self, handler: MangaSite):
        if issubclass(handler, MangaSite):
            if handler not in self.__custom_handlers:
                self.__custom_handlers.append(handler)
        else:
            raise Exception('<MangaSite> required')
