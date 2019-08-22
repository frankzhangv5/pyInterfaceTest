# coding=utf-8
import os
import unittest
import HTMLTestRunner

from framework.util.Config import Config
from framework.util.Email import Email
from framework.util.Log import Log

TAG = os.path.basename(__file__)

class TestRunner:
    _instance = None

    def __init__(self):
        pass

    def setUpTestSuite(self, case_dir):
        testsuite = unittest.TestSuite()
        testmodules = []

        discover = unittest.defaultTestLoader.discover(case_dir, pattern='*.py', top_level_dir=None)
        testmodules.append(discover)

        if len(testmodules) > 0:
            for module in testmodules:
                for testcase in module:
                    testsuite.addTest(testcase)
        else:
            return None

        return testsuite


    @classmethod
    def _getInstance(cls):
        if cls._instance is None:
            cls._instance = TestRunner()
        return cls._instance

    @classmethod
    def run(cls, case_dir=os.path.join(os.getcwd(), "testcases")):
        instance = cls._getInstance()

        Log.i(TAG, "********TEST START********")
        fp = None
        try:
            testsuite = instance.setUpTestSuite(case_dir)
            if testsuite is not None:
                report_dir = Config.get("REPORT", "dir")
                if report_dir is None:
                    report_dir = os.path.join(os.getcwd(), "result")
                else:
                    if os.path.exists(report_dir) and os.path.isdir(report_dir):
                        try:
                            os.removedirs(report_dir)
                            Log.i(TAG, "remove dir: " + report_dir)
                        except Exception as e:
                            Log.e(TAG, "remove failed: " + report_dir + ", exception: " + str(e))
                    try:
                        os.mkdir(report_dir)
                    except Exception as e:
                        Log.e(TAG, "mkdir failed: " + report_dir + ", exception: " + str(e))

                report_file = Config.get("REPORT", "file")
                if report_file is None:
                    report_file = "report.html"

                report_path = os.path.join(report_dir, report_file)
                fp = open(report_path, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(testsuite)
            else:
                Log.i(TAG, "No  testcase was found .")
        except Exception as ex:
            Log.e(TAG, str(ex))
        finally:
            if fp is not None:
                fp.close()

            # send test report by email
            email_switch = Config.get("EMAIL", "switch")
            if email_switch == 'on':
                Email.send()
            elif email_switch == 'off':
                Log.i(TAG, "Do not send report via email")
            else:
               Log.e(TAG, "Unknow state.")

            Log.i(TAG, "********TEST END**********")

if __name__ == "__main__":
    TestRunner.run()