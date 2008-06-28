from zope.interface import implements, Interface
from zope import schema

from plone.dexterity import api

class IPyPage(api.Schema):
    
    title = schema.TextLine(title=u"Title")
    
    summary = schema.Text(title=u"Summary",
                          description=u"Summary of the body",
                          readonly=True)
    
    body = schema.Text(title=u"Body text")

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
        return "%s..." % self.body[:30]
        
    def Description(self):
        return self.summary