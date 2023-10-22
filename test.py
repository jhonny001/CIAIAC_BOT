import unittest
from config import BOT_TOKEN, CHAT_ID, URL_YEARS
from functions import send_message_to_telegram


class TelegramSender(unittest.TestCase):
    token = BOT_TOKEN
    chat_id = CHAT_ID

    def test_send_message(self):
        r = send_message_to_telegram("TEST", self.token, self.chat_id)
        self.assertEqual(200, r.status_code)

