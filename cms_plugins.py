import json
import markdown
import re
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import MarkdownImage, MarkdownFile, Markdown, MarkdownHistory

class MarkdownImageInline(admin.TabularInline):
    model = MarkdownImage
    extra = 1

class MarkdownFileInline(admin.TabularInline):
    model = MarkdownFile
    extra = 1

class MarkdownCMSPlugin(CMSPluginBase):
    name = _('Markdown')
    model = Markdown
    render_template = "markdown.html"
    change_form_template = "change_form_template.html"
    inlines = [MarkdownImageInline, MarkdownFileInline]

    def __init__(self, model=None, admin_site=None):
        super(MarkdownCMSPlugin, self).__init__(model, admin_site)

    def change_view(self, request, object_id, extra_context=None):
        def escape(text):
            html_escape_table = {
                "&": "&amp;",
                '"': "&quot;",
                "'": "&apos;",
                ">": "&gt;",
                "<": "&lt;",
                }
            return "".join(html_escape_table.get(c,c) for c in text)

        history_data =  [ {'content' : escape(mh.content), 'css' : escape(mh.css), 'date' : mh.date.strftime("%d. %B %Y %H:%M")}
                    for mh in MarkdownHistory.objects.filter(markdown=Markdown.objects.get(pk=object_id)).order_by('-date')]
        if extra_context is None:
            extra_context = {}
        extra_context.update({
            'history' : json.dumps(history_data)
        })
        return super(MarkdownCMSPlugin, self).change_view(request, object_id, extra_context)

    def render(self, context, instance, placeholder):
        content_html = markdown.markdown(instance.content)

        def repl(match):
            alias = match.group(1)
            for markdownfile in MarkdownFile.objects.filter(markdown=instance, alias=alias):
                return markdownfile.file.url
            for markdownimage in MarkdownImage.objects.filter(markdown=instance, alias=alias):
                return markdownimage.image.url

            return ''

        content_html = re.sub("{{\s*(.*?)\s*}}", repl, content_html)

        context.update({
            'content' : content_html,
            'css' : instance.css,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(MarkdownCMSPlugin)

