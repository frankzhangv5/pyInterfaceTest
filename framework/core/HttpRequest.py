# coding=utf-8
import os
import requests
import socket

from framework.util.Log import Log

TAG = os.path.basename(__file__)

class HttpRequest:

    def __init__(self, host, port=-1, timeout=60, headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}):
        self.host = host
        self.timeout = timeout
        self.headers = headers
        self.port = port;
        if (port == -1):
            if (host.startswith("https")):
                self.port = 443
            else:
                self.port = 80

    def get(self, api, params):
        url = "%s:%d/%s" % (self.host, self.port, api)
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=float(self.timeout), verify=False)
            response.raise_for_status()
            Log.i(TAG, "[get] response code: " + str(response.status_code))
            return response
        except socket.timeout:
            Log.e(TAG, "[get] Time out!")
            return None
        except requests.RequestException as e:
            Log.e(TAG, "[get] RequestException: " + str(e))
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self, api, data):
        url = "%s:%d/%s" % (self.host, self.port, api)
        Log.i(TAG, "[post] request url: " + url)
        try:
            response = requests.post(url, headers=self.headers, data=data,
                                     timeout=float(self.timeout) , verify=False)
            response.raise_for_status()
            Log.i(TAG, "[post] response code: " + str(response.status_code))
            return response
        except socket.timeout:
            Log.e(TAG, "[post] Time out!")
            return None
        except requests.RequestException as e:
            Log.e(TAG, "[post] RequestException: " + str(e))
            return None

if __name__ == "__main__":
    request = HttpRequest(host="https://cn.bing.com")
    response = request.get("search", {"q" : "python+requests"})
    response.encoding = "utf-8"
    fd = open("bing.html")
    fd.write(response.content)
    fd.close()