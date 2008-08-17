import unittest
import example.dexterity

from zope.testing import doctestunit
from zope.component import testing, getMultiAdapter

from zope.component import createObject

from zope.lifecycleevent import modified

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite, onsetup

from example.dexterity.page import IPage
from example.dexterity.pypage import PyPage

@onsetup
def setup_product():
    zcml.load_config('meta.zcml', example.dexterity)
    zcml.load_config('configure.zcml', example.dexterity)

    # NOTE: There is no need to call ztc.installPackage() since this package
    # is not a Zope 2 product.
    
setup_product()
ptc.setupPloneSite(products=['example.dexterity'])

class IntegrationTests(ptc.PloneTestCase):
    
    def test_adding(self):
        
        # Ensure that invokeFactory() works as with normal types
        
        self.folder.invokeFactory('example.filefolder', 'ff')
        self.folder.invokeFactory('example.pypage', 'pp')
        self.folder.invokeFactory('example.schemapage', 'sp')
        self.folder.invokeFactory('example.ttwpage', 'tp')
        self.folder.invokeFactory('example.fspage', 'fp')
    
    def test_folderish(self):
        
        # Demonstrate that the filefolder type is indeed folderish, and
        # that is supports dict notation for accessing content.
        
        self.folder.invokeFactory('example.filefolder', 'ff')
        self.folder.ff.invokeFactory('example.ttwpage', id="tp", title="Test title")
        
        self.failUnless('tp' in self.folder.ff)
        self.assertEquals('Test title', self.folder.ff['tp'].Title())
        
    def test_attributes_and_reindexing(self):
        
        # Demonstrate that dynamic types such as example.ttwpage 
        # automatically get the attributes specified in their model, and
        # that content is reindexed when an IObjectModified event is fired.
        
        self.folder.invokeFactory('example.ttwpage', 'tp', title="Old title")
        self.assertEquals("Old title", self.folder.tp.title)
        self.assertEquals(u"Default body text", self.folder.tp.body)
        
        self.folder.tp.title = "New Title"
        self.folder.tp.body = u"Sample body"
        modified(self.folder.tp)
        
        self.assertEquals("New Title", self.folder.tp.title)
        
        results = self.portal.portal_catalog(Title="New title")
        self.assertEquals(1, len(results))
        self.assertEquals("Sample body", list(results)[0].getObject().body)
    
    def test_grokking_of_schema(self):
        
        # Demonstrate that schemata defined with a model() are grokked,
        # causing fields from the XML file to be added to the interface.
        
        self.failUnless('title' in IPage)
        self.assertEquals(u"Page title", IPage['title'].title)
    
    def test_grokking_of_class(self):
        
        # Demonstrate that classes deriving from Item or Container
        # will be initialised 
        
        self.failUnless(hasattr(PyPage, 'body'))
        self.assertEquals("Body text goes here", PyPage.body)
        
    def test_grokking_of_forms(self):
        request = self.folder.REQUEST
        addview = getMultiAdapter((self.folder, request), name=u"add-example.fspage")
        addform = addview._form
        fspage = addform.createAndAdd({})
        editview = getMultiAdapter((fspage, request), name=u"edit")

def test_suite():
    return unittest.TestSuite([unittest.makeSuite(IntegrationTests)])