import hmac
import tempfile
import shutil

import zope.interface
import zope.component
import z3c.form.testing
from zope.annotation import IAnnotations
from Zope2.App.zcml import load_config

from plone.keyring.interfaces import IKeyManager
from plone.protect.authenticator import _getUserName
from plone.protect.authenticator import sha

from Products.PloneTestCase import PloneTestCase as ptc
from Products.CMFCore.utils import getToolByName

from pmr2.z3cform.tests import base
from pmr2.z3cform.tests.base import IPMR2TestRequest, TestRequest
import pmr2.testing


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
