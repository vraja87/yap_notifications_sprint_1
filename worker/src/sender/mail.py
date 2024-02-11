from abc import ABC, abstractmethod
from email.message import EmailMessage

import aiosmtplib as aiosmtplib
import backoff
from src.config import config_mail
from src.logger import logger


class AbstractNotification(ABC):

    @abstractmethod
    async def send(self):
        pass


class MailNotification(AbstractNotification):
    def __init__(self, user_notification: dict):
        self.user_notification = user_notification
        self.from_email = f'{config_mail.login}@{config_mail.domain}'
        self.message = EmailMessage()

    def prepare_message(self):
        self.message['From'] = self.from_email
        self.message['To'] = self.user_notification['contact']
        self.message['Subject'] = self.user_notification['subject']
        self.message.set_content(self.user_notification["content"])

    @backoff.on_exception(backoff.expo, aiosmtplib.SMTPException, max_tries=3)
    async def send(self):
        if config_mail.real_send:
            await aiosmtplib.send(
                self.message,
                hostname=config_mail.host,
                port=config_mail.port,
                use_tls=True,
                username=config_mail.login,
                password=config_mail.password
            )
        logger.info(f'Mail sent to {self.user_notification["contact"]}')
