import tempfile
import shutil

import zope.interface
import zope.component
import z3c.form.testing
from zope.annotation import IAnnotations
from Zope2.App.zcml import load_config

from Products.PloneTestCase import PloneTestCase as ptc

import pmr2.testing


class IPMR2TestRequest(zope.interface.Interface):
    """\
    Marker for PMR2 test request
    """


class TestRequest(z3c.form.testing.TestRequest):
    """\
    Customized TestRequest to mimic missing actions.
    """

    # IAnnotations applied by plone.z3cform test case.
    zope.interface.implements(IAnnotations, IPMR2TestRequest)
    def __init__(self, *a, **kw):
        super(TestRequest, self).__init__(*a, **kw)
        if self.form:
            self.method = 'POST'

    def __setitem__(self, key, value):
        self.form[key] = value

    def __getitem__(self, key):
        try:
            return super(TestRequest, self).__getitem__(key)
        except KeyError:
            return self.form[key]

    def getApplicationURL(self):
        # XXX compatibility with the more strict redirection introduced
        # with zope.publisher-3.12, http.redirect's untrusted attribute.
        return 'http://nohost:80'


class TestCase(ptc.PloneTestCase):
    """\
    For standard tests.
    """


class DocTestCase(ptc.FunctionalTestCase):
    """\
    For doctests.
    """

    def setUp(self):
        load_config('test.zcml', pmr2.testing)
        super(DocTestCase, self).setUp()
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        super(DocTestCase, self).tearDown()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

