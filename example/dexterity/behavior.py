from persistent import Persistent

from zope.interface import implements, Interface
from zope.component import adapts

from zope import schema

from zope.annotation.interfaces import IAnnotatable
from zope.annotation import factory

from BTrees.OOBTree import OOSet

class ITaggingBehavior(Interface):
    """Behavior interface to make a type support tagging.
    If this is listed as enabled in the FTI, then we will be able to
    adapt a content item of the given type to this interface.
    """
    
    enabled = schema.Bool(title=u"Enable tagging")
    
    def add(tag):
        """Add a tag
        """
    
    def remove(tag):
        """Remove a tag
        """
    
    def tags():
        """List tags
        """
# Implementation of the behavior
    
class ITaggingAnnotations(Interface):
    """Specifies annotations that store tagging data
    """
    
    enabled = schema.Bool(title=u"Enabled")
    tags = schema.Set(title=u"Tags", value_type=schema.TextLine(title=u"Tag"))

class TaggingAnnotations(Persistent):
    """Persistent storage for tags
    """
    
    implements(ITaggingAnnotations)
    adapts(IAnnotatable)
    
    def __init__(self):
        self.enabled = False
        self.tags = OOSet()

TaggingAnnotationsFactory = factory(TaggingAnnotations)

class TaggingBehavior(object):
    """Implementation of the behavior that stores data in annotations.
    """

    implements(ITaggingBehavior)
    
    def __init__(self, context):
        self.data = ITaggingAnnotations(context)
        
    def _get_enabled(self):
        return self.data.enabled
    def _set_enabled(self, value):
        self.data.enabled = value
    enabled = property(_get_enabled, _set_enabled)
    
    def add(self, tag):
        self.data.tags.add(tag)
        
    def remove(self, tag):
        self.data.tags.remove(tag)
        
    def tags(self):
        return list(self.data.tags)