import requests
import re
import json
import os
import demjson

class HttpMethod():
    def __init__(self):
        self.headers = {
            'Content-Type': "application/json"
        }
        self.s = requests.session()

    def set_header(self,headers):
        for key,value in headers.items():
            self.headers[key] = value

    def httpget(self,testdata):
        try:
            if testdata['head'] !="":
                self.set_header(eval(testdata['head']))
            url = testdata['apiAddress']
            r = self.s.get(url, verify=False, headers = self.headers)
            return r
        except Exception as e:
            print(str(e))
            raise Exception(e)

    def httppost(self,testdata):
        try:
            if testdata['head'] !="":
                self.set_header(eval(testdata['head']))
            body = json.dumps(eval(testdata['data']))
            r = self.s.post(testdata['apiAddress'], data=body, verify=False, headers = self.headers)
            return r
        except Exception as e:
            print(str(e))
            raise Exception(e)

# if __name__ == '__main__':
#     rf = RequestFunc()
