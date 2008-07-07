from persistent import Persistent

from zope.interface import implements, Interface
from zope.component import adapts

from zope import schema

from zope.annotation.interfaces import IAnnotatable
from zope.annotation import factory

from BTrees.OOBTree import OOSet

class ITagging(Interface):
    """Behavior interface to make a type support tagging.
    """
    
    enabled = schema.Bool(title=u"Tagging enabled",
                          required=False,
                          default=True)
    
    tags = schema.List(title=u"Tags",
                       description=u"Tags for this object",
                       value_type=schema.Choice(values=["Tag 1", "Tag 2", "Tag 3"]),
                       required=False)

class TaggingAnnotations(Persistent):
    """Persistent storage for tags in annotations
    """
    
    implements(ITagging)
    adapts(IAnnotatable)
    
    def __init__(self):
        self.enabled = True
        self.tags = OOSet()

# Use the factory from zope.annotation to support persistent storage of tag data.
Tagging = factory(TaggingAnnotations)