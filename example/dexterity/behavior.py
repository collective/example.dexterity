from persistent import Persistent

from zope.interface import implements, directlyProvides, Interface
from zope.component import adapts

from zope import schema

from zope.annotation.interfaces import IAnnotatable
from zope.annotation import factory

from plone.dexterity import api

from BTrees.OOBTree import OOSet

class ITagging(api.Schema):
    """Behavior interface to make a type support tagging.
    """
    
    api.order_before(enabled='description')
    api.omitted('tags')
    api.fieldset('tagging', label=u"Tagging", fields=['enabled', 'tags'])
    
    enabled = schema.Bool(title=u"Tagging enabled",
                          required=False,
                          default=True)
    
    tags = schema.List(title=u"Tags",
                       description=u"Tags for this object",
                       value_type=schema.Choice(values=["Tag 1", "Tag 2", "Tag 3"]),
                       required=False)

# Specify that the fields in this interface should be used in the add/edit forms.
# We could also have registered an adapter from ITagging to IFormFieldProvider
# if we wanted to use different fields. 
directlyProvides(ITagging, api.IFormFieldProvider)

class TaggingAnnotations(Persistent):
    """Persistent storage for tags in annotations. This uses the "persistent 
    adapter" pattern seen in zope.annotation's README.txt. Of course, a
    regular adapter from context to ITagging would work just as well, but 
    there'd be more work persisting values. If you use a simple adapter,
    don't forget to make __init__() take a 'context' parameter.
    """
    
    implements(ITagging)
    adapts(IAnnotatable)
    
    def __init__(self):
        self.enabled = True
        self.tags = OOSet()

# Use the factory from zope.annotation to support persistent storage of tag data.
Tagging = factory(TaggingAnnotations)