"""This file contains an example of a behavior that makes content taggable.

The behavior itself is registered using the <plone:behavior /> directive in
configure.zcml. 

We first define an interface that describes the behavior, and then mark it
with IFormFieldProvider. This tells Dexterity to include the fields from this
interface when rendering its standard add- and edit forms.

Since behaviors can be turned on or off on different types, we cannot make a
custom form for each one. Instead, we make use of directives that give hints
about how and where the fields should be rendered. 

Finally, we make use of a zope.annotation factory to create an adapter backed
by a persistent storage. When the behavior is looked up, the caller will be
given a persistent object that provides the ITagging interface and stores its
values in an annotation. Other behaviors may not need this type of persistent
storage, but it is quite convenient to use this style of factory for behaviors
that do.
"""

from persistent import Persistent

from zope.interface import implements, alsoProvides
from zope.component import adapts

from zope import schema

from zope.annotation.interfaces import IAnnotatable
from zope.annotation import factory

from plone.directives import dexterity

from BTrees.OOBTree import OOSet

class ITagging(dexterity.Schema):
    """Behavior interface to make a type support tagging.
    """
    dexterity.order_before(enabled='description')
    dexterity.fieldset('tagging', label=u"Tagging", fields=['enabled', 'tags'])
    
    enabled = schema.Bool(title=u"Tagging enabled",
                          required=False,
                          default=True)
    
    tags = schema.List(title=u"Tags",
                       description=u"Tags for this object",
                       value_type=schema.Choice(values=["Tag 1", "Tag 2", "Tag 3"]),
                       required=False)

alsoProvides(ITagging, dexterity.IFormFieldProvider)

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