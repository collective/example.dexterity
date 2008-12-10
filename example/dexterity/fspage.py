"""This file contains an example of a more conventional filesystem page type.
It has a schema, add- and edit- forms using z3c.form and a class.

We first define a standard schema. Deriving from form.Schema is optional,
but demonstrates conistency and makes it possible to use the type of
directives seen in pypage.py, if you so wish.

Then, we define the content class. This derives from dexterity.Item (there is
also dexterity.Container for folderish types). The constructor ensures that
all the fields in the interface are set correctly.

We also specify the name of the type's factory, using the grok.name()
directive. This will cause an IFactory utility to be registered that knows
how to create instances of this class. If this is omitted, a local factory
utility will be created with the same id as the type's FTI when the FTI is
installed. However, a global utility is slightly faster and means there's no
chance of a "stale" local component ending up in the local component registry.
Also, we need to specify the name of the factory when we register the add form
below, so it makes sense to define them both here. The factory is explicitly 
set in in the example.fspage.xml GenericSetup file.

Next, we define a view called @@view. This will look for a template in
fspage_templates/view.pt, since the view class is called "View" and this
module is called "fspage.py".

We then define custom add and edit forms, using z3c.form via the
plone.z3cform integration package. Here, we use z3c.form's "groups" support
to split our form fields into two fieldsets. Both the add form and edit form
will be grokked to provide the appropriate wrappers required by plone.z3cform
and CMF, and register the appropriate adapters.

Note how in the add form, we have to specify the name of the factory, via the
grok.name() directive. This is because the CMF ++add++ traverser looks for
an add view adapter (on context, request, fti) with the same name as the
factory for the content being constructed. For the edit form, we specify the
context as the IFSPage interface.
"""

from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

class IFSPage(form.Schema):
    
    body = schema.Text(title=u"Body text",
                       required=False,
                       default=u"Body text goes here")

    details = schema.Text(title=u"Details",
                          required=False)

class FSPage(dexterity.Item):
    grok.implements(IFSPage)
    grok.name('example.fspage')
    
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
    grok.name('example.fspage')
    
    fields = fields
    groups = (ExtraFieldsGroup,)

class EditForm(dexterity.EditForm):
    grok.context(IFSPage)
    
    fields = fields
    groups = (ExtraFieldsGroup,)