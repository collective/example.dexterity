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

from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

class IPyPage(form.Schema):
    
    # The default fieldset
    
    summary = schema.Text(
            title=u"Summary",
            description=u"Summary of the body",
            readonly=True
        )
    
    body = schema.Text(
            title=u"Body text",
            required=False,
            default=u"Body text goes here"
        )
    form.widget(body=WysiwygFieldWidget)
    
    # Extra information fieldset
    form.fieldset('extra', label=u"Extra info", fields=['footer', 'dummy'])    
    
    footer = schema.Text(
            title=u"Footer text",
            required=False
        )
    form.widget(footer=WysiwygFieldWidget)
    
    dummy = schema.Text(
            title=u"Dummy"
        )
    form.omitted('dummy')
    
    # A hidden field, not in any fieldset
    
    secret = schema.TextLine(
            title=u"Secret",
            default=u"Secret stuff"
        )
    form.mode(secret='hidden')


class PyPage(dexterity.Item):
    grok.implements(IPyPage)

    @property
    def summary(self):
        if self.body:
            return "%s..." % self.body[:30]
        else:
            return ""
        
    def Description(self):
        return self.summary