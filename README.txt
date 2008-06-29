Introduction
============

This package contains example types as defined using the Dexterity 
system. Please see the plone.dexterity package for more information about
Dexterity.

All types are installable using GenericSetup.

The types defined here include:

 example.ttwpage
 
    A non-folderish type with a simple schema that is defined entirely
    through-the-web, in a property inside the FTI.

 example.filefolder
 
    A folderish type with a simple schema that is defined in a file,
    folder.xml.
    
 example.schemapage
 
    A non-folderish type that is defined from a "real" filesystem interface.
    The interface is populated with fields held the page.xml model file.
    A custom view is registered for the type's interface, but there is no
    unique type class.
    
 example.pypage
 
    A non-folderish page type that has a "real" filesystem interface created
    entirely with Python, and a specific filesystem class. There is no XML
    involved at all.
    
Other things to note:

 - This package is not a Zope 2 product, i.e. there's no 
   <five:registerPackage /> directive.

 - The package is "grokked" with the line <grok:grok package="." /> in
   configure.zcml. This takes care of populating the IPage interface
   in page.py with fields from its model file (page.xml) and setting up
   the content class in pypage.py.
   
 - The custom view used for IPage is called "view", thus overriding the 
   default view registered for all Dexterity content.

 - The view defined using page.pt assumes the attributes of IPage are 
   available on the context, i.e. it uses TAL statements like "context/body".