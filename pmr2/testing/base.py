import tempfile
import shutil

from Zope2.App.zcml import load_config

from Products.PloneTestCase import PloneTestCase as ptc
from Products.CMFCore.utils import getToolByName

from pmr2.z3cform.tests import base
# BBB should mark this import location as deprecated.
from pmr2.z3cform.tests.base import TestRequest
from pmr2.z3cform.tests.base import IPMR2TestRequest


class TestCase(ptc.PloneTestCase):
    """\
    For standard tests.
    """


class DocTestCase(base.DocTestCase):
    """
    Provide shortcut to publish content and create new temporary
    directory for testing.
    """

    def setUp(self):
        import pmr2.testing
        load_config('test.zcml', pmr2.testing)
        super(DocTestCase, self).setUp()
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        super(DocTestCase, self).tearDown()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _publishContent(self, obj):
        # shortcut that works for default workflow types.
        # XXX figure out a better way to force workflow states right
        # without messing with permissions.
        pw = getToolByName(self.portal, "portal_workflow")
        self.setRoles(('Manager',))
        pw.doActionFor(obj, "publish")
        self.setRoles(('Member', 'Authenticated',))
