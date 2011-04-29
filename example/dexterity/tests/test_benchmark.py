import gc
from time import time
import unittest

from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five import zcml

from plone.app.dexterity.tests.layer import DexterityLayer

class DexterityExampleLayer(DexterityLayer):
    @classmethod
    def setUp(cls):
        import example.dexterity.tests
        zcml.load_config('test.zcml', example.dexterity.tests)

    @classmethod
    def tearDown(cls):
        pass

BENCHMARK_REPS = 20
def benchmark(func):
    def benchmarked_func(self):
        # prime the pumps
        func(self)
        # temporarily disable garbage collection
        gc.disable()
        times = []
        for i in xrange(0, BENCHMARK_REPS):
            t0 = time()
            func(self)
            t1 = time()
            elapsed = t1 - t0
            times.append(elapsed)
        gc.enable()
        print "\n%32s:  best: %.4f  average: %.4f\n" % (
            func.__name__, min(times), sum(times) / BENCHMARK_REPS)
    return benchmarked_func

ptc.setupPloneSite(products=['example.dexterity'])

class Benchmarks(ptc.FunctionalTestCase):
    
    layer = DexterityExampleLayer

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
        self.browser.open(self.portal_url + '++add++example.ttwpage')

    @benchmark
    def test_create_AT_page(self):
        self.browser.open(self.portal_url + 'createObject?type_name=Document')
        self.browser.getControl('Title').value = 'atdoc2'
        self.browser.getControl('Save').click()
        self.failUnless('atdoc2' in self.browser.url)

    @benchmark
    def test_create_dexterity_page(self):
        self.browser.open(self.portal_url + '++add++example.ttwpage')
        self.browser.getControl('Title').value = 'dexdoc2'
        self.browser.getControl('Save').click()
        self.failUnless('dexdoc2' in self.browser.url)

    @benchmark
    def test_AT_page_editform(self):
        self.browser.open(self.portal_url + 'atdoc/edit')
    
    @benchmark
    def test_dexterity_page_editform(self):
        self.browser.open(self.portal_url + 'dexdoc/edit')

    @benchmark
    def test_edit_AT_page(self):
        self.browser.open(self.portal_url + 'atdoc/edit')
        self.browser.getControl('Title').value = 'New atdoc title'
        self.browser.getControl('Save').click()
        self.failUnless('atdoc' in self.browser.url)

    @benchmark
    def test_edit_dexterity_page(self):
        self.browser.open(self.portal_url + 'dexdoc/edit')
        self.browser.getControl('Title').value = 'New dexdoc title'
        self.browser.getControl('Save').click()
        self.failUnless('dexdoc' in self.browser.url)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Benchmarks))
    return suite
