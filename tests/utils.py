from vimeo.vimeo import VimeoBlock

from xblock.field_data import DictFieldData
from xblock.test.tools import TestRuntime

def createVimeoXBlockTestInstance():
    field_data = DictFieldData({'data': 'Safe <b>html</b>'})
    runtime = TestRuntime(field_data=field_data)

    return VimeoBlock(runtime, scope_ids=None)
