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
        addform = addview.form_instance
        fspage = addform.createAndAdd({})
        editview = getMultiAdapter((fspage, request), name=u"edit")

from Products.Five.testbrowser import Browser
from time import time
import gc

BENCHMARK_REPS = 50
def benchmark(func):
    def benchmarked_func(self):
        # prime the pumps
        func(self)
        # temporarily disable garbage collection
        gc.disable()
        t0 = time()
        for i in xrange(0, BENCHMARK_REPS):
            func(self)
        t1 = time()
        gc.enable()
        elapsed = t1 - t0
        print "\n%s: %s\n" % (func.__name__, elapsed)
    return benchmarked_func

class Benchmarks(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.browser = Browser()
        self.browser.handleErrors = False
        self.portal_url = 'http://nohost/plone/'
        
        # log in
        self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
        self.browser.addHeader('Authorization', 'Basic root:secret')
        self.setRoles(['Manager'])
        
        # add a sample page (AT and dexterity)
        self.app.plone.invokeFactory('Document', 'atdoc')
        self.app.plone.invokeFactory('example.ttwpage', 'dexdoc')

    @benchmark
    def test_view_AT_page(self):
        self.browser.open(self.portal_url + 'atdoc')
    
    @benchmark
    def test_view_dexterity_page(self):
        self.browser.open(self.portal_url + 'dexdoc')
    
    @benchmark
    def test_AT_page_addform(self):
        self.browser.open(self.portal_url + 'createObject?type_name=Document')
    
    @benchmark
    def test_dexterity_page_addform(self):
        self.browser.open(self.portal_url + '@@add-dexterity-content/example.ttwpage')

    @benchmark
    def test_create_AT_page(self):
        self.browser.open(self.portal_url + 'createObject?type_name=Document')
        self.browser.getControl('Title').value = 'atdoc2'
        self.browser.getControl('Save').click()
        self.failUnless('atdoc2' in self.browser.url)

    @benchmark
    def test_create_dexterity_page(self):
        self.browser.open(self.portal_url + '@@add-dexterity-content/example.ttwpage')
        self.browser.getControl('Title').value = 'dexdoc2'
        self.browser.getControl('Save').click()
        # XXX change this once we have title-to-id functionality
        self.failUnless('example.ttwpage' in self.browser.url)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    suite.addTest(unittest.makeSuite(Benchmarks))
    return suite
