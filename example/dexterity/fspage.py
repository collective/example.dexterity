"""This file contains an example of a more conventional filesystem page type.
It has a schema, add- and edit- forms using z3c.form and a class.
"""

from five import grok
from plone.dexterity import api as dexterity

from zope import schema

from z3c.form import group, field
from plone.z3cform import layout

from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

# 1. Define schema interface

class IFSPage(dexterity.Schema):
    
    title = schema.TextLine(title=u"Title")
    
    description = schema.Text(title=u"Description",
                          description=u"Summary of the body")
    
    body = schema.Text(title=u"Body text",
                       required=False,
                       default=u"Body text goes here")

    details = schema.Text(title=u"Details",
                          required=False)

# 2. Define content class

class FSPage(dexterity.Item):
    grok.implements(IFSPage)
    dexterity.portal_type('example.fspage')
    
    def __init__(self, id=None, title=None, description=None, body=None, details=None):
        self.id = id # required - or call super() with this argument
        self.title = title
        self.description = description
        self.body = body
        self.details = details

# 4. Define view. The template is automatically located in
#  fspage_templates/view.pt in this directory.

class View(grok.View):
    grok.name('view')
    grok.require('zope2.View')

# 5. Define add and edit forms. Here we also show how to set up fieldsets
#  using groups

fields = field.Fields(IFSPage, omitReadOnly=True).omit('details')
fields['body'].widgetFactory = WysiwygFieldWidget

class ExtraFieldsGroup(group.Group):
    fields = field.Fields(IFSPage).select('details')
    label = u"Extra fields"

class AddForm(dexterity.DefaultAddForm):
    fields = fields
    groups = (ExtraFieldsGroup,)
    portal_type = 'example.fspage'

# TODO: Turn into simple wrapper, and make optional with grokker
import plone.dexterity.browser.add
class AddView(plone.dexterity.browser.add.DefaultAddView):
    form = AddForm

class EditForm(dexterity.DefaultEditForm):
    fields = fields
    groups = (ExtraFieldsGroup,)

EditView = layout.wrap_form(EditForm) # TODO: Make optional with grokker
