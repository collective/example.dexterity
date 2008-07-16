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
    involved at all. Grok-like directives are used to give hints about how to
    render add- and edit-forms, which are based on generic implementations.
    The grokker will also register a default factory and add view adapter
    factory.
    
 example.fspage
 
    A non-folderish page type that has a "real" filesystem interface created
    entirely with Python, a specific filesystem class, and filesystem add-
    and edit forms. Again, there is no XML involved. The only local component
    that will be registered is the local utility used to look up the FTI
    object.
    
    
Other things to note:

 - This package is not a Zope 2 product, i.e. there's no 
   <five:registerPackage /> directive.

 - The package is "grokked" with the line <grok:grok package="." /> in
   configure.zcml. This takes care of populating the IPage interface
   in page.py with fields from its model file (page.xml), setting up
   the content classes in pypage.py and fspage.py and performing a few other
   boilerplate registrations.
   
 - The custom view used for IPage is called "view", thus overriding the 
   default view registered for all Dexterity content.

 - The custom edit view used for IFSPage is called "edit", thus overriding the
   default view registered for all Dexterity content.

 - The views defined in e.g. page.pt assumes that standard schema attributes
   are  available on the context, i.e. they use TAL statements like
   "context/body".