from zope.interface import implements
from zope import schema

from zope.component.factory import Factory

from plone.dexterity import api
from plone.dexterity.browser import add, edit

from z3c.form import group, field

from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

# This file contains an example of a more conventional filesystem page type
# The only thing that's done implicitly is the grokking of the class to
# do the five:registerClass dance, and even that could be done with ZCML.

# TODO: To make this more pleasant, we could take some patterns from Grok.
# For example:
#   
#   - Don't require separate form and view classes for add/edit forms
#   - Register add/edit forms using grokkers for views
#   - Register default view using grokker and tie to template by name
#   - Register factory utility using grokker for class

class IFSPage(api.Schema):
    
    title = schema.TextLine(title=u"Title")
    
    description = schema.Text(title=u"Description",
                          description=u"Summary of the body")
    
    body = schema.Text(title=u"Body text",
                       required=False,
                       default=u"Body text goes here")

    details = schema.Text(title=u"Details",
                          required=False)

fields = field.Fields(IFSPage, omitReadOnly=True).omit('details')
fields['body'].widgetFactory = WysiwygFieldWidget

class ExtraFieldsGroup(group.Group):
    fields = field.Fields(IFSPage).select('details')
    label = u"Extra fields"

class AddForm(add.DefaultAddForm):
    fields = fields
    groups = (ExtraFieldsGroup,)
    
class AddView(add.DefaultAddView):
    form = AddForm
    
    def __init__(self, context, request):
        super(AddView, self).__init__(context, request, portal_type='example.fspage')
    
class EditForm(edit.DefaultEditForm):
    fields = fields
    groups = (ExtraFieldsGroup,)
    
class EditView(edit.DefaultEditView):
    form = EditForm

class FSPage(api.Item):
    implements(IFSPage)
    portal_type = 'example.fspage'
    
    def __init__(self, id=None, title=None, description=None, body=None, details=None):
        super(FSPage, self).__init__(id)
        self.title = title
        self.description = description
        self.body = body
        self.details = details
        
# If this is not created and registered, a default implementation will be provided
FSPageFactory = Factory(FSPage)