# coding=utf-8

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from framework.util.Log import Log
from framework.util.Config import Config


class Email:
    _instance = None

    def __init__(self):
        self.host = Config.get("EMAIL", "mail_host")
        self.port = Config.get("EMAIL", "mail_port")
        self.user = Config.get("EMAIL", "mail_user")
        self.password = Config.get("EMAIL", "mail_pass")
        self.sender = Config.get("EMAIL", "sender")
        self.subject = "[%s][%s]" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), Config.get("EMAIL", "subject"))
        self.receiver = Config.get("EMAIL", "receiver") # seprated by ;

        self.msg = MIMEMultipart('related')
        self.msg['subject'] = self.subject
        self.msg['from'] = self.sender
        self.msg['to'] = self.receiver

    def handleContent(self):
        content = Config.get("EMAIL", "content")
        html_content = Config.get("EMAIL", "html_content")

        if html_content is not None:
            if os.path.exists(html_content) and os.path.isfile(html_content):
                f = open(html_content, "r")
                content = f.read()
                f.close()
                content_plain = MIMEText(content, 'html', 'UTF-8')
                self.msg.attach(content_plain)
                return

        if content is not None:
            self.msg['content'] = content
        else:
            self.msg['content'] = ""
        return

    def handleAttachment(self):
        attachment = Config.get("EMAIL", "attachment")
        if  attachment is not None:
            if os.path.exists(attachment) and os.path.isfile(attachment):
                print "find attachment:" + attachment
                f = open(attachment, 'rb').read()
                filehtml = MIMEText(f, 'base64', 'utf-8')
                filehtml['Content-Type'] = 'application/octet-stream'
                filehtml['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(attachment)
                self.msg.attach(filehtml)

    @classmethod
    def _getInstance(cls):
        if cls._instance is None:
            cls._instance = Email()
        return cls._instance

    @classmethod
    def send(cls):
        instance = cls._getInstance()
        instance.handleContent()
        instance.handleAttachment()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(instance.host, instance.port)
            smtp.login(instance.user, instance.password)
            smtp.sendmail(instance.sender, instance.receiver, instance.msg.as_string())
            smtp.quit()
            Log.i("send", "send email succed.")
        except Exception as ex:
            Log.e("send", str(ex))


if __name__ == "__main__":
    Email.send()