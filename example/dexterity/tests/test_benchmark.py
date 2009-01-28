import gc
from time import time
import unittest

from Products.Five import zcml
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import example.dexterity


@onsetup
def setup_product():
    zcml.load_config('meta.zcml', example.dexterity)
    zcml.load_config('configure.zcml', example.dexterity)

setup_product()
ptc.setupPloneSite(products=['example.dexterity'])

BENCHMARK_REPS = 1
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


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Benchmarks))
    return suite
