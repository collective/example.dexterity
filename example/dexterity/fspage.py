"""This file contains an example of a more conventional filesystem page type.
It has a schema, add- and edit- forms using z3c.form and a class.

We first define a standard schema. Deriving from dexterity.Schema is optional,
but demonstrates conistency and makes it possible to use the type of
directives seen in pypage.py, if you so wish.

Then, we define the content class. This derives from dexterity.Item (there is
also dexterity.Container for folderish types) and declares its portal type
with the portal_type class variable. The construct ensures that all
the fields in the interface are set correctly.

Next, we define a view called @@view. This will look for a template in
fspage_templates/view.pt, since the view class is called "View" and this
module is called "fspage.py".

We then define custom add and edit forms, using z3c.form via the
plone.z3cform integration package. Here, we use z3c.form's "groups" support
to split our form fields into two fieldsets.
"""

from five import grok
from plone.directives import dexterity

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

class IFSPage(dexterity.Schema):
    
    body = schema.Text(title=u"Body text",
                       required=False,
                       default=u"Body text goes here")

    details = schema.Text(title=u"Details",
                          required=False)

class FSPage(dexterity.Item):
    grok.implements(IFSPage)
    portal_type = 'example.fspage'
    
    def __init__(self, id=None, body=None, details=None):
        self.id = id # required - or call super() with this argument
        self.body = body
        self.details = details

class View(grok.View):
    grok.context(IFSPage)
    grok.require('zope2.View')

fields = field.Fields(IFSPage, omitReadOnly=True).omit('details')
fields['body'].widgetFactory = WysiwygFieldWidget

class ExtraFieldsGroup(group.Group):
    fields = field.Fields(IFSPage).select('details')
    label = u"Extra fields"

class AddForm(dexterity.AddForm):
    portal_type = 'example.fspage'
    fields = fields
    groups = (ExtraFieldsGroup,)

class EditForm(dexterity.EditForm):
    grok.context(IFSPage)
    fields = fields
    groups = (ExtraFieldsGroup,)