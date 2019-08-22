# coding=utf-8
import os
from xml.etree import ElementTree


class Xml:
    _instance = None

    def __init__(self):
       pass

    def _get(self, xml_path, tag, attr, value):
        list = []
        tree = ElementTree.parse(xml_path)
        for elem in tree.findall(tag):
            val = elem.get(attr)
            if val == value:
                for c in elem.getchildren():
                    list.append(c.text)
        return "/".join(list)

    @classmethod
    def _getInstance(cls):
        if cls._instance is None:
            cls._instance = Xml()
        return cls._instance

    @classmethod
    def get(cls, xml_path, tag, attr, value):
        return cls._getInstance()._get(xml_path, tag, attr, value)


if __name__ == "__main__":
    print Xml.get(os.path.join(os.getcwd(), "testcases","config", "api.xml"), "url", "name", "login")
