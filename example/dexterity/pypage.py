from zope.interface import implements, Interface
from zope import schema

from plone.dexterity.api import Schema, Item

class IPyPage(Schema):
    
    title = schema.TextLine(title=u"Title")
    
    summary = schema.Text(title=u"Summary",
                          description=u"Summary of the body",
                          readonly=True)
    
    body = schema.Text(title=u"Body text")

class PyPage(Item):
    implements(IPyPage)
    
    title = u""
    body = u""
    
    @property
    def summary(self):
        return "%s..." % self.body[:30]
        
    def Description(self):
        return self.summary