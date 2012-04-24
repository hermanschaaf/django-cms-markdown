from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from urls import urlpatterns

class MarkdownApphook(CMSApp):
    name = _("Markdown")
    urls = [urlpatterns]

apphook_pool.register(MarkdownApphook)


