from logging import getLogger

import requests


logger = getLogger(__name__)


class BittrexError(Exception):
    """
    Неизвестная ошибка при запросе API Bittrex
    """


class BittrexClient(object):

    def __init__(self):
        self.base_url = "https://api.bittrex.com/api/v1.1"

    def _request(self, method, params):
        url = self.base_url + method

        try:
            r = requests.get(url=url, params=params)
            result = r.json()
        except Exception:
            logger.exception("Bittrex error")
            pass

        if result.get("success"):
            # Успешный запрос
            return result
        else:
            # Некорректный запрос
            logger.error("Request error: %s", result.get("message"))

    def get_ticker(self, pair):
        params = {
            "market": pair
        }
        return self._request(method="/public/getticker", params=params)
