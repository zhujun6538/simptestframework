from .unittest_script import SimpleTest
from .. import urls
import os
import datetime
from BeautifulReport import BeautifulReport as bf
import unittest
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_suite(suites, suitename):
    testsuite = unittest.TestSuite()
    for suite in suites:
        casedict = suite['case']
        apidic = suite['api']
        testsuite.addTest(SimpleTest(methodName=casedict['examineType'], casedict=casedict, apidic=apidic))
    report_path = os.path.join(urls.get_media_root(), 'report')
    # report_path = os.path.join(BASE_DIR, 'report')
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        run = bf(testsuite)
        run.title = suitename + now
        filename = suitename + now + '.html'
        run.report( description='', filename=filename, report_dir=report_path)
    except Exception as e:
        print(e)
    return run

# if __name__ == '__main__':
#     newdata = [{'case': {'id': 1, 'casename': '测试用例', 'relateapi': '测试接口1', 'examineType': 'only_check_status',
#                'expecthttpCode': '200', 'expectdata': 'get_succees', 'createtime': '2020-04-05', 'creater': 'admin'},
#       'api': {'id': 1, 'name': '测试接口1', 'requestType': 'GET', 'apiAddress': 'http://127.0.0.1:8000/testapi/',
#               'head': "{\r\n'xxx':'xxx'\r\n}", 'data': '', 'description': '', 'createtime': '2020-04-05 08:19:12',
#               'creater': 'admin'}}, {
#          'case': {'id': 3, 'casename': '测试用例2', 'relateapi': '测试接口2', 'examineType': 'only_check_status',
#                   'expecthttpCode': '200', 'expectdata': 'value is right', 'createtime': '2020-04-06',
#                   'creater': 'admin'},
#          'api': {'id': 2, 'name': '测试接口2', 'requestType': 'POST', 'apiAddress': 'http://127.0.0.1:8000/testapi/',
#                  'head': '', 'data': "{'value':'i',}", 'description': '', 'createtime': '2020-04-09 08:38:42',
#                  'creater': 'admin'}}]
#     run_suite(newdata,'testsuite')