"""This interface is used by the example.schemapage type. The interface
below is "real", and you can register views and adapters for it. It
will be populated with schema fields read from page.xml in this 
directory when the package is grokked.
"""

from five import grok
from plone.dexterity import api as dexterity

class IPage(dexterity.Schema):
    dexterity.model("page.xml")
    
    # It is possible to add additional fields and methods can be added here
    # if necessary. However, without a custom class, we usually can't
    # promise new methods.

class View(grok.View):
    grok.context(IPage)
    grok.require('zope2.View')