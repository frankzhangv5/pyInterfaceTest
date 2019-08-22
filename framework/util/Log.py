# coding=utf-8
import os
import logging
from datetime import datetime

TAG = os.path.basename(__file__)

class Log:
    _instance = None
    _console_print = True

    def __init__(self, log_dir=os.path.join(os.getcwd(), "result"), log_level=logging.INFO):
        if os.path.exists(log_dir):
            try:
                os.removedirs(log_dir)
            except Exception as e:
                pass

        try:
            os.mkdir(log_dir)
        except Exception as e:
            pass

        log_path = os.path.join(log_dir, "log_" + str(datetime.now().strftime("%Y%m%d_%H%M%S")) + ".txt")

        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

        # defined handler
        handler = logging.FileHandler(log_path)
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("log path: " + log_path)

    @classmethod
    def _getInstance(cls):
        if cls._instance is None:
            cls._instance = Log()
        return cls._instance

    @classmethod
    def enter(cls, msg):
        if cls._console_print:
            print "--------enter " + str(msg) + "--------"
        cls._getInstance().logger.info("--------enter " + msg + "--------")

    @classmethod
    def exit(cls, msg):
        if cls._console_print:
            print "--------exit " + str(msg) + "--------"
        cls._getInstance().logger.info("--------exit " + msg + "--------")

    @classmethod
    def d(cls, tag, msg):
        if cls._console_print:
            print "%-10s: %s" % (str(tag), str(msg))
        cls._getInstance().logger.debug("%-10s: %s" % (tag, msg))

    @classmethod
    def i(cls, tag, msg):
        if cls._console_print:
            print "%-10s: %s" % (str(tag), str(msg))
        cls._getInstance().logger.info("%-10s: %s" % (tag, msg))

    @classmethod
    def e(cls, tag, msg):
        if cls._console_print:
            print "%-10s: %s" % (str(tag), str(msg))
        cls._getInstance().logger.error("%-10s: %s" % (tag, msg))

if __name__ == "__main__":
    TAG = "LOG"
    Log.d(TAG, "debug level message")
    Log.i(TAG, "info level message")
    Log.e(TAG, "error level message")
    Log.enter("test")
    Log.exit("test")

