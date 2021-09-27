import sys
import logging
import pkg_resources
import requests

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment
from django.template import Context, Template

log = logging.getLogger(__name__)

def isPython27():
    """
    Checks if it is Python 2.7 or Not
    """
    return (sys.version_info[0] < 3)

if isPython27():
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

    unicode = str

class VimeoBlock(XBlock):
    """
    An XBlock providing oEmbed capabilities for video from Vimeo
    """

    href = String(help="URL of the video page at the provider", default=None,
                  scope=Scope.content)
    width = Integer(help="Width of the video", default=800,
                    scope=Scope.content)
    height = Integer(help="Height of the video", default=511,
                     scope=Scope.content)
    watched = Integer(help="How many times the student has watched it?",
                      default=0, scope=Scope.user_state)
    display_name = String(
        display_name="Display Name", help="Display name for this block.",
        default="Vimeo",
        scope=Scope.settings)

    icon_class = 'video'

    unsupported_error_msg = "Unsupported video provider"
    exception_error_msg = "Error getting video from provider"

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def load_resource(self, path):
        """
        Gets Content of a Resource and Encodes it to UTF-8 For Python 2.7
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return unicode(resource_content)

    def create_fragment(self, html, context={}, js=[], css=[], initialize=None):
        """
        Create an XBlock Fragment

        Creates an XBlock Fragment given an HTML file path, 
        an optional Context, optional JS file paths, optional CSS file paths,
        and an optional Initialize JS value

        Arguments:
            html (str): HTML File Path
            context (dict): Optional Context for HTML File
            js (list): Optional List of JS File Paths
            css (list): Optional List of CSS File Paths
            initialize (str): Optional Initialize Value for JS

        Returns:
            Fragment 
        """
        if isPython27():
            html_str = self.load_resource(html)
        else:
            html_str = self.resource_string(html)
        html = Template(html_str)

        frag = Fragment(html.render(Context(context)))

        for stylesheet in css:
            frag.add_css(self.resource_string(stylesheet))

        for script in js:
            frag.add_javascript(self.resource_string(script))

        if initialize:
            frag.initialize_js(initialize)

        return frag

    def student_view(self, context=None):
        """
        The primary view of the VimeoBlock, shown to students
        when viewing courses.
        """
        provider, embed_code = self.get_embed_code_for_url(self.href)

        context = {
            'display_name': self.display_name,
            'embed_code': embed_code
        }

        html_file = "static/html/vimeo.html"

        css_stylesheets = [
            "static/css/vimeo.css",
        ]

        if provider == "vimeo.com":
            js_scripts = [
                "static/js/lib/froogaloop.min.js",
                "static/js/src/vimeo.js",
            ]

            initialize_value = "VimeoBlock"

            return self.create_fragment(html_file,
                context=context,
                js=js_scripts,
                css=css_stylesheets,
                initialize=initialize_value
            )
        else:
            return self.create_fragment(html_file,
                context=context,
                css=css_stylesheets
            )

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        context = {
            'href': self.href or '',
            'width': self.width,
            'height': self.height,
            'display_name': self.display_name
        }

        html_file = "static/html/vimeo_edit.html"

        js_scripts = [
            "static/js/src/vimeo_edit.js",
        ]

        initialize_value = "VimeoEditBlock"

        return self.create_fragment(html_file,
            context=context,
            js=js_scripts,
            initialize=initialize_value
        )

    def get_embed_code_for_url(self, url):
        """
        Get the code to embed from the oEmbed provider
        """
        hostname = url and urlparse(url).hostname
        params = {
            'url': url,
            'format': 'json',
            'width': self.width,
            'height': self.height
        }

        if hostname == 'vimeo.com':
            oembed_url = 'http://vimeo.com/api/oembed.json'
            params['api'] = True
        else:
            return hostname, '<p>{message} ({hostname})</p>'.format(
                message=self.unsupported_error_msg, 
                hostname=hostname
            )

        try:
            r = requests.get(oembed_url, params=params)
            r.raise_for_status()
        except Exception as e:
            return hostname, '<p>{message} ({error})</p>'.format(
                message=self.exception_error_msg,
                error=e
            )
        response = r.json()

        return hostname, response['html']

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.href = data.get('href')
        self.width = data.get('width')
        self.height = data.get('height')
        self.display_name = data.get('display_name')

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
                    <vimeo href="https://vimeo.com/96321771" width="800" />
                </vertical_demo>
            """)
        ]
