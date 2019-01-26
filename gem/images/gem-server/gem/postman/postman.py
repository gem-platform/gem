import smtplib


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

    def send(self, to, message):
        self.__server.sendmail(self.__sender, to, message)

    def close(self):
        self.__server.quit()
