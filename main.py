# coding=utf-8
import os
from framework.util.Log import Log
from framework.util.Config import Config
from framework.util.Email import Email
from framework.util.Xml import Xml
from framework.util.Xlsx import Xlsx

from framework.core.HttpRequest import HttpRequest
from framework.testrunner.TestRunner import TestRunner

if __name__ == "__main__":
    print "****************start********************"
    # Log.i("Main", "log in main")

    # print Config.get("EMAIL", "sender")

    # request = HttpRequest(host="https://cn.bing.com")
    # response = request.get("search", {"q" : "python+requests"})
    # response.encoding = "utf-8"
    # fd = open(os.path.join(os.getcwd(), "bing.html"), "w")
    # fd.write(response.content)
    # fd.close()

    # Email.send()

    # TestRunner.run()
    # print Xml.get(os.path.join(os.getcwd(), "testcases","config", "api.xml"), "url", "name", "login")

    # print Xlsx.rows(os.path.join(os.getcwd(), "testcases", "config", "testcase.xlsx"),
    #                "login",
    #                ["case_name", "method", "token", "email", "password", "code"])
    TestRunner.run(os.path.join(os.getcwd(), "testcases"))

    print "****************end**********************"