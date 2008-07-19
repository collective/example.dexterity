"""This file contains an example of a more conventional filesystem page type.
It has a schema, add- and edit- forms using z3c.form and a class. It also
registers a factory utility explicitly, although it would have gained one
anyway.
"""

from zope.interface import implements
from zope import schema

from zope.component.factory import Factory

from plone.dexterity import api
from plone.dexterity.browser import add, edit

from z3c.form import group, field

from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

# 1. Define schema interface

class IFSPage(api.Schema):
    
    title = schema.TextLine(title=u"Title")
    
    description = schema.Text(title=u"Description",
                          description=u"Summary of the body")
    
    body = schema.Text(title=u"Body text",
                       required=False,
                       default=u"Body text goes here")

    details = schema.Text(title=u"Details",
                          required=False)

# 2. Define fields and groups (fieldsets)

fields = field.Fields(IFSPage, omitReadOnly=True).omit('details')
fields['body'].widgetFactory = WysiwygFieldWidget

class ExtraFieldsGroup(group.Group):
    fields = field.Fields(IFSPage).select('details')
    label = u"Extra fields"

# 3. Define add form and add view that uses it

class AddForm(add.DefaultAddForm):
    fields = fields
    groups = (ExtraFieldsGroup,)
    portal_type = 'example.fspage'
    
class AddView(add.DefaultAddView):
    form = AddForm

# 4. Define edit form and edit view that uses it

class EditForm(edit.DefaultEditForm):
    fields = fields
    groups = (ExtraFieldsGroup,)
    
class EditView(edit.DefaultEditView):
    form = EditForm

# 5. Define content class

class FSPage(api.Item):
    implements(IFSPage)
    api.portal_type('example.fspage')
    
    def __init__(self, id=None, title=None, description=None, body=None, details=None):
        super(FSPage, self).__init__(id)
        self.title = title
        self.description = description
        self.body = body
        self.details = details
        
# 6. Define factory (optional)
FSPageFactory = Factory(FSPage)