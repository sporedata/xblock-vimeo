import logging

import pkg_resources
import requests

from urlparse import urlparse
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

log = logging.getLogger(__name__)


class VimeoBlock(XBlock):
    """
    An XBlock providing oEmbed capabilities for video from Vimeo
    """

    href = String(help="URL of the video page at the provider", default=None,
                  scope=Scope.content)
    maxwidth = Integer(help="Maximum width of the video", default=800,
                       scope=Scope.content)
    maxheight = Integer(help="Maximum height of the video", default=450,
                        scope=Scope.content)
    watched = Integer(help="How many times the student has watched it?",
                      default=0, scope=Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the VimeoBlock, shown to students
        when viewing courses.
        """
        provider, embed_code = self.get_embed_code_for_url(self.href)

        html_str = self.resource_string("static/html/vimeo.html")
        frag = Fragment(unicode(html_str).format(self=self,
                        embed_code=embed_code))

        css_str = self.resource_string("static/css/vimeo.css")
        frag.add_css(unicode(css_str))

        if provider == 'vimeo.com':
            js_str = self.resource_string("static/js/lib/froogaloop.min.js")
            frag.add_javascript(unicode(js_str))
            js_str = self.resource_string("static/js/src/vimeo.js")
            frag.add_javascript(unicode(js_str))
            frag.initialize_js('VimeoBlock')

        return frag

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        html_str = self.resource_string("static/html/vimeo_edit.html")
        href = self.href or ''
        frag = Fragment(unicode(html_str).format(href=href,
                        maxwidth=self.maxwidth, maxheight=self.maxheight))

        js_str = self.resource_string("static/js/src/vimeo_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('VimeoEditBlock')

        return frag

    def get_embed_code_for_url(self, url):
        """
        Get the code to embed from the oEmbed provider
        """
        hostname = url and urlparse(url).hostname
        params = {
            'url': url,
            'format': 'json',
            'maxwidth': self.maxwidth,
            'maxheight': self.maxheight
        }

        if hostname == 'vimeo.com':
            oembed_url = 'http://vimeo.com/api/oembed.json'
            params['api'] = True
        else:
            return hostname, '<p>Unsupported video provider ({0})</p>'.format(hostname)

        try:
            r = requests.get(oembed_url, params=params)
            r.raise_for_status()
        except Exception as e:
            return hostname, '<p>Error getting video from provider ({error})</p>'.format(error=e)
        response = r.json()

        return hostname, response['html']

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.href = data.get('href')
        self.maxwidth = data.get('maxwidth')
        self.maxheight = data.get('maxheight')

        return {'result': 'success'}

    @XBlock.json_handler
    def mark_as_watched(self, data, suffix=''): # pylint: disable=unused-argument
        """
        Called upon completion of the video
        """
        if not data.get('watched'):
            log.warn('not watched yet')
        else:
            self.watched += 1

        return {'watched': self.watched}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("vimeo",
            """\
                <vertical_demo>
                    <vimeo href="https://vimeo.com/96321771" maxwidth="800" />
                </vertical_demo>
            """)
        ]
