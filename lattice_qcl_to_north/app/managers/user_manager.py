import json

import requests
from decouple import config

from app.managers.redis_manager import redis_manager

from app import logger

log = logger.get_logger()

"""
Please use triple quotes for code documentation
"""


class UserManager:

    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.ons_oauth2_bearer = self.get_oauth2_bearer()
        self.organisation_id = "qarbon"


    @staticmethod
    def get_oauth2_bearer():
        """
        Description:  Function to get ONS bearer token.
        Parameters : 
        Returns: Returns bearer token.
        """
        payload = config('ONS_PAYLOAD')
        auth = config('ONS_AUTH')
        headers = {
            'Authorization': auth,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = "https://8147918.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
        # please define constant url in .env file or constant.py file
        response = (requests.request("POST", url, headers=headers, data=payload)).json()
        bearer = response["access_token"]
        headers = {
            'Authorization': f'Bearer {bearer}'
        }
        return headers
    
