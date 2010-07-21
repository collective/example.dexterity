import unittest
import example.dexterity

from zope.component import getMultiAdapter

from zope.lifecycleevent import modified

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from example.dexterity.page import IPage
from example.dexterity.pypage import PyPage


@onsetup
def setup_product():
    zcml.load_config('meta.zcml', example.dexterity)
    zcml.load_config('configure.zcml', example.dexterity)

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
    
    def test_folderish_default_view(self):
        
        self.folder.invokeFactory('example.filefolder', 'ff')
        self.folder.ff.invokeFactory('example.ttwpage', id="tp", title="TTW Page")
        self.folder.ff.setDefaultPage('tp')
        self.assertEquals('tp', self.folder.ff.defaultView())
    
    def test_attributes_and_reindexing(self):
        
        # Demonstrate that dynamic types such as example.ttwpage 
        # automatically get the attributes specified in their model, and
        # that content is reindexed when an IObjectModified event is fired.
        
        self.folder.invokeFactory('example.ttwpage', 'tp', title="Old title")
        self.assertEquals("Old title", self.folder.tp.title)
        self.assertEquals(u"Default body text", self.folder.tp.body.output)
        
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
        
        self.failUnless('body' in IPage)
        self.assertEquals(u"Body text", IPage['body'].title)
            
    def test_grokking_of_forms(self):
        request = self.folder.REQUEST
        addview = self.folder.restrictedTraverse("++add++example.fspage")
        addform = addview.form_instance
        fspage = addform.createAndAdd({})
        editview = getMultiAdapter((fspage, request), name=u"edit")

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite
