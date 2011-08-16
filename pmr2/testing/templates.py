import os.path
import z3c.form.interfaces
from plone.z3cform.templates import ZopeTwoFormTemplateFactory

from pmr2.testing.base import IPMR2TestRequest

path = lambda p: os.path.join(os.path.dirname(__file__), p)

standalone_form_factory = ZopeTwoFormTemplateFactory(path('form.pt'),
        form=z3c.form.interfaces.IForm,
        request=IPMR2TestRequest,
    )

# subform_factory = FormTemplateFactory(path('subform.pt'),
#         form=z3c.form.interfaces.ISubForm,
#         request=IPMR2TestRequest,
#     )
