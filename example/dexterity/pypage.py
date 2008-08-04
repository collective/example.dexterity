"""This file contains an example of a type that uses a custom class (PyPage)
and a Python-only interface (IPyPage). We could have loaded IPyPage from
a model file, of course - see page.py.

Note that if the schema promises zope.schema fields that are not set on
the class, the grokker for dexterity.Item (or dexterity.Container) will set these on
the class, initialising them to field defaults.

In the example below, we are using various directives to give hints about
how the form should be rendered. We normally would only use one or two of
these for convenience. For complex forms, it is easier to just use the
z3c.form API. Take a look at fspage.py to see a more complete example of that.
"""

from zope.interface import implements, Interface
from zope import schema

from plone.dexterity import api as dexterity
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

class IPyPage(dexterity.Schema):
    
    dexterity.omitted('dummy')
    dexterity.mode(secret='hidden')
    dexterity.fieldset('extra', label=u"Extra info", fields=['footer', 'dummy'])    
    dexterity.widget(body='plone.app.z3cform.wysiwyg.WysiwygFieldWidget', footer=WysiwygFieldWidget)
    
    title = schema.TextLine(title=u"Title")
    
    summary = schema.Text(title=u"Summary",
                          description=u"Summary of the body",
                          readonly=True)
    
    body = schema.Text(title=u"Body text",
                       required=False,
                       default=u"Body text goes here")
                       
    footer = schema.Text(title=u"Footer text",
                       required=False)
    
    dummy = schema.Text(title=u"Dummy")
    
    
    secret = schema.TextLine(title=u"Secret", default=u"Secret stuff")
    

class PyPage(dexterity.Item):
    implements(IPyPage)
    dexterity.portal_type('example.pypage')

    @property
    def summary(self):
        if self.body:
            return "%s..." % self.body[:30]
        else:
            return ""
        
    def Description(self):
        return self.summary