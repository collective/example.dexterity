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