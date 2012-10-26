import hmac
import tempfile
import shutil

import zope.interface
import zope.component
import z3c.form.testing
from zope.app.publication.zopepublication import BeforeTraverseEvent
from zope.annotation import IAnnotations
from Zope2.App.zcml import load_config

from plone.browserlayer.layer import mark_layer
from plone.browserlayer.utils import register_layer
from plone.keyring.interfaces import IKeyManager
from plone.protect.authenticator import _getUserName
from plone.protect.authenticator import sha

from Products.PloneTestCase import PloneTestCase as ptc
from Products.CMFCore.utils import getToolByName

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
        self.environ = {}
        if self.form:
            self.method = 'POST'
            self._set_authenticator()

    def __setitem__(self, key, value):
        self.form[key] = value

    def __getitem__(self, key):
        try:
            return super(TestRequest, self).__getitem__(key)
        except KeyError:
            return self.form[key]

    def _set_authenticator(self):
        manager = zope.component.queryUtility(IKeyManager)
        if not manager:
            # Since the key manager is not installed, authenticator 
            # should not be working anyway.
            return
        secret = manager.secret()
        user = _getUserName()
        auth = hmac.new(secret, user, sha).hexdigest()
        self['_authenticator'] = auth

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
        register_layer(IPMR2TestRequest, 'pmr2.app.testing')

    def markLayer(self):
        # Helper method to trigger the mark layer event.
        event = BeforeTraverseEvent(self.portal, self.portal.REQUEST)
        mark_layer(self.portal, event)

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

