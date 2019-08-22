# coding=utf-8
import os
import unittest
import paramunittest
import json

from framework.core.HttpRequest import HttpRequest
from framework.util.Log import Log
from framework.util.Config import Config
from framework.util.Email import Email
from framework.util.Xml import Xml
from framework.util.Xlsx import Xlsx

TAG = os.path.basename(__file__)

login_rows = Xlsx.rows(os.path.join(os.getcwd(), "testcases", "config", "testcase.xlsx"),
                   "login",
                   ["case_name", "method", "token", "email", "password", "result", "code", "msg"])

@paramunittest.parametrized(*login_rows)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, email, password, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param email:
        :param password:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.email = str(email)
        self.password = str(password)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = {}

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        Log.d(TAG, "setUp")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        api = Xml.get(os.path.join(os.getcwd(), "testcases","config", "api.xml"), "url", "name", "login")

        params = {"email": self.email, "password": self.password}

        # get visitor token
        if self.token == '0':
            token = Config.get("HEADERS", "token_v")
        elif self.token == '1':
            token = Config.get("HEADERS", "token_u")
        else:
            token = None

        headers = {'content-type': 'application/json;charset=utf-8',
                   "Accept":"application/json;q=0.9,image/webp,*/*;q=0.8",
                   "token": str(token)}

        request = HttpRequest(host = Config.get("HTTP", "host"), headers=headers)

        if self.method == "post":
            self.response = request.post(api, params)
        elif self.method == "get":
            self.response = request.get(api, params)

        if self.response is not None:
            Log.d(TAG, "[testLogin] response url: %s\nresponse code: %d" % (self.response.url, self.response.status_code))
            self.response.encoding = "utf-8"
            self.write_response(self.response)
            try:
                self.info = self.response.json()
            except Exception as e:
                self.result = "-1"
                self.info['code'] = -1
                self.info['msg'] = "error"
                pass


            if self.result == '0':
                email = self.get_value_from_response(self.info, 'member', 'email')
                self.assertEqual(email, self.email)
                self.assertEqual(self.info['code'], self.code)
                self.assertEqual(self.info['msg'], self.msg)
            elif self.result == '1':
                self.assertEqual(self.info['code'], self.code)
                self.assertEqual(self.info['msg'], self.msg)
            else:
                self.assertNotEqual(self.result, "-1")

    def tearDown(self):
        info = self.info
        if info['code'] == 0:
            # get uer token
            token_u = self.get_value_from_response(info, 'member', 'token')
            # set user token to config file
            Config.set("HEADERS", "token_u", token_u)

        Log.i(TAG, "[tearDown] case:%s, code:%d, msg:%s" % (self.case_name, self.info['code'], self.info['msg']))

    def write_response(self, response):
        fd = open(os.path.join(os.getcwd(), "result", self.case_name + ".html"), "w")
        fd.write(self.response.content)
        fd.close()

    def get_value_from_response(self, json, name1, name2):
        """
        get value by key
        :param json:
        :param name1:
        :param name2:
        :return:
        """
        info = json['info']
        group = info[name1]
        value = group[name2]
        return value