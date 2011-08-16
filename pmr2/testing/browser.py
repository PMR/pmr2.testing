import os.path
from z3c.form import tests
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class GroupTemplate(object):

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return ViewPageTemplateFile('simple_groupedit.pt', os.path.dirname(
            tests.__file__))(self.context)
