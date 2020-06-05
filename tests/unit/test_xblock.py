import sys

if sys.version_info[0] >= 3:
    import unittest
    from unittest import mock as mock
else:
    import mock as mock
    import unittest2 as unittest

from mock import patch, MagicMock

from requests.exceptions import Timeout

from vimeo.vimeo import VimeoBlock

from web_fragments.fragment import Fragment

from tests.utils import createVimeoXBlockTestInstance

class TestXBlock(unittest.TestCase):
    """
    Unit tests for `vimeo_xblock`
    """
    def setUp(self):
        self.vimeo_block = createVimeoXBlockTestInstance()

    @patch("requests.get")
    def test_vimeo_url_get_embeded_code(self, mock_request):
        mock_request.return_value.status_code = 200

        url = "https://vimeo.com/306558851"
        _, res = self.vimeo_block.get_embed_code_for_url(url)

        self.assertNotIn(self.vimeo_block.exception_error_msg, res)
        self.assertNotIn(self.vimeo_block.unsupported_error_msg, res)

    @patch("requests.get")
    def test_youtube_url_get_embedded_code(self, mock_request):
        mock_request.return_value.status_code = 200

        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        _, res = self.vimeo_block.get_embed_code_for_url(url)

        self.assertIn(self.vimeo_block.unsupported_error_msg, res)

    @patch("requests.get")
    def test_bad_url_get_embedded_code(self, mock_request):
        mock_request.side_effect = Timeout()

        url = "https://vimeo.com/306558851"
        _, res = self.vimeo_block.get_embed_code_for_url(url)

        self.assertIn(self.vimeo_block.exception_error_msg, res)

    @patch("{0}.VimeoBlock.create_fragment".format(__name__))
    @patch("{0}.VimeoBlock.get_embed_code_for_url".format(__name__))
    def test_student_view(self, mock_embeded_code, mock_create_fragment):
        mock_embeded_code.return_value = ("", "")
        mock_create_fragment.return_value = Fragment()

        self.assertIsInstance(self.vimeo_block.student_view(None), Fragment)
        mock_create_fragment.assert_called_once()

    @patch("{0}.VimeoBlock.create_fragment".format(__name__))
    @patch("{0}.VimeoBlock.get_embed_code_for_url".format(__name__))
    def test_studio_view(self, mock_embeded_code, mock_create_fragment):
        mock_embeded_code.return_value = ("", "")
        mock_create_fragment.return_value = Fragment()

        self.assertIsInstance(self.vimeo_block.student_view(None), Fragment)
        mock_create_fragment.assert_called_once()

if __name__ == "__main__":
    unittest.main()
