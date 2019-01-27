import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Postman:
    """
    EMail sender.
    """

    def __init__(self, sender):
        self.__server = None
        self.__sender = sender

    def connect(self, host, port):
        self.__server = smtplib.SMTP(host, port)

    def login(self, login, password):
        self.__server.login(login, password)

    def send(self, to, subject, message, plain_message=None):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.__sender
        msg["To"] = to

        part1 = MIMEText(plain_message, "plain")
        part2 = MIMEText(message, "html")

        msg.attach(part1)
        msg.attach(part2)

        self.__server.sendmail(self.__sender, to, msg.as_string())

    def close(self):
        self.__server.quit()
