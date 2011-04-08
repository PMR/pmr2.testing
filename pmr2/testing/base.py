import tempfile
import shutil

import zope.interface
import zope.component
import z3c.form.testing
from zope.annotation import IAnnotations

from Products.PloneTestCase import PloneTestCase as ptc


class TestRequest(z3c.form.testing.TestRequest):
    """\
    Customized TestRequest to mimic missing actions.
    """

    # XXX why do we need this implements?
    zope.interface.implements(IAnnotations)
    def __init__(self, *a, **kw):
        super(TestRequest, self).__init__(*a, **kw)

    def __setitem__(self, key, value):
        self.form[key] = value

    def __getitem__(self, key):
        try:
            return super(TestRequest, self).__getitem__(key)
        except KeyError:
            return self.form[key]


class TestCase(ptc.PloneTestCase):
    """\
    For standard tests.
    """


class DocTestCase(ptc.FunctionalTestCase):
    """\
    For doctests.
    """

    def setUp(self):
        super(DocTestCase, self).setUp()
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        super(DocTestCase, self).tearDown()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

