from zope.interface import implements, Interface
from zope import schema

from plone.dexterity import api
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

# This file contains an example of a type that uses a custom class (PyPage)
# and a Python-only interface (IPyPage). We could have loaded IPyPage from
# a model file, of course - see page.py.
# 
# Note that if the schema promises zope.schema fields that are not set on
# the class, the grokker for api.Item (or api.Container) will set these on
# the class, initialising them to field defaults.

class IPyPage(api.Schema):
    
    api.omitted('dummy')
    api.mode(secret='hidden')
    api.fieldset('extra', label=u"Extra info", fields=['footer', 'dummy'])    
    api.widget(body='plone.app.z3cform.wysiwyg.WysiwygFieldWidget',
               footer=WysiwygFieldWidget)
    
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
    

class PyPage(api.Item):
    implements(IPyPage)

    # Use the meta_type directive if you require the class to be registered 
    # as a Zope 2 class with a meta_type and the rest. The default add
    # permission is cmf.AddPortalContent, but you can use the add_permission
    # directive to specify a different one.
    # 
    # api.meta_type("PyPage")
    # api.add_permission("cmf.AddPortalContent")
    
    @property
    def summary(self):
        if self.body:
            return "%s..." % self.body[:30]
        else:
            return ""
        
    def Description(self):
        return self.summary