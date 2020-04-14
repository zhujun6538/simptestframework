import logging
import unittest
from .httpmethod import HttpMethod
import re

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class ParametrizedTestCase(unittest.TestCase):
    def __init__(self,methodName = 'assertEqual_func',casedict = None,apidic = None):
        super(ParametrizedTestCase,self).__init__(methodName)
        self.case = casedict
        self.api = apidic

class SimpleTest(ParametrizedTestCase):

    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    @classmethod
    def setUpClass(self):
        logger.info('start')

    @classmethod
    def tearDownClass(self):
        logger.info('end')

    def assertEqual_func(self):
        '''完全校验'''
        casedict = self.case
        apidic = self.api
        self._testMethodDoc = casedict['casename']
        if apidic['requestType'] == 'GET':
            rsp = HttpMethod().httpget(apidic)
        elif apidic['requestType'] == 'POST':
            rsp = HttpMethod().httppost(apidic)
        try:
            cont = rsp.content.decode('utf-8')
            code = str(rsp.status_code)
        except Exception as e:
            logger.info('fail')
            raise self.failureException(e)
        try:
            self.assertEqual(code, casedict['expecthttpCode'],msg=casedict['casename']+'响应码验证结果'+str(code)+'='+str(casedict['expecthttpCode']))
            self.assertEqual(casedict['expectdata'],cont,msg=casedict['casename']+'响应内容验证结果'+str(cont)+'='+str(casedict['expectdata']))
            logger.info('pass')
        except AssertionError as e:
            logger.info('fail')
            raise self.failureException(e)

    def assertNotEqual_func(self):
        '''完全校验'''
        casedict = self.case
        apidic = self.api
        self._testMethodDoc = casedict['casename']
        if apidic['requestType'] == 'GET':
            rsp = HttpMethod().httpget(apidic)
        elif apidic['requestType'] == 'POST':
            rsp = HttpMethod().httppost(apidic)
        try:
            cont = rsp.content.decode('utf-8')
            
            code = str(rsp.status_code)
            
            
        except Exception as e:
            logger.info('fail')
            raise self.failureException(e)
        try:
            self.assertEqual(code, casedict['expecthttpCode'])
            self.assertNotEqual(casedict['expectdata'],cont)
            logger.info('pass')
        except AssertionError as e:
            logger.info('fail')
            raise self.failureException(e)

    def assertIn_func(self):
        '''完全校验'''
        casedict = self.case
        apidic = self.api
        self._testMethodDoc = casedict['casename']
        if apidic['requestType'] == 'GET':
            rsp = HttpMethod().httpget(apidic)
        elif apidic['requestType'] == 'POST':
            rsp = HttpMethod().httppost(apidic)
        try:
            cont = rsp.content.decode('utf-8')
            
            code = str(rsp.status_code)
            
            
        except Exception as e:
            logger.info('fail')
            raise self.failureException(e)
        try:
            self.assertEqual(code, casedict['expecthttpCode'])
            self.assertIn(casedict['expectdata'],cont)
            logger.info('pass')
        except AssertionError as e:
            logger.info('fail')
            raise self.failureException(e)

    def assertNotIn_func(self):
        '''完全校验'''
        casedict = self.case
        apidic = self.api
        self._testMethodDoc = casedict['casename']
        if apidic['requestType'] == 'GET':
            rsp = HttpMethod().httpget(apidic)
        elif apidic['requestType'] == 'POST':
            rsp = HttpMethod().httppost(apidic)
        try:
            cont = rsp.content.decode('utf-8')
            
            code = str(rsp.status_code)
            
            
        except Exception as e:
            logger.info('fail')
            raise self.failureException(e)
        try:
            self.assertEqual(code, casedict['expecthttpCode'])
            self.assertNotIn(casedict['expectdata'],cont)
            logger.info('pass')
        except AssertionError as e:
            logger.info('fail')
            raise self.failureException(e)

    def assertRegexpMatches_func(self):
        '''完全校验'''
        casedict = self.case
        apidic = self.api
        self._testMethodDoc = casedict['casename']
        if apidic['requestType'] == 'GET':
            rsp = HttpMethod().httpget(apidic)
        elif apidic['requestType'] == 'POST':
            rsp = HttpMethod().httppost(apidic)
        try:
            cont = rsp.content.decode('utf-8')
            
            code = str(rsp.status_code)
            
            
        except Exception as e:
            logger.info('fail')
            raise self.failureException(e)
        try:
            self.assertEqual(code, casedict['expecthttpCode'])
            self.assertRegexpMatches(cont,casedict['expectdata'])
            logger.info('pass')
        except AssertionError as e:
            logger.info('fail')
            raise self.failureException(e)
