# coding=utf-8
import os
import codecs
import configparser


class Config:
    _instance = None

    def __init__(self, config_path=os.path.join(os.getcwd(), "config.ini")):
        fd = open(config_path, "r")
        data = fd.read()
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(config_path, "w")
            file.write(data)
            file.close()
        fd.close()

        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.config_path = config_path

    @classmethod
    def _getInstance(cls):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    @classmethod
    def get(cls, sector, key):
        try:
            return cls._getInstance().config.get(sector, key)
        except Exception as e:
            return None


    @classmethod
    def set(cls, sector, key , value):
        instance = cls._getInstance()
        instance.config.set(sector, key , value)
        with open(instance.config_path, 'w+') as f:
            instance.config.write(f)

if __name__ == "__main__":
    print Config.get("EMAIL", "sender")
