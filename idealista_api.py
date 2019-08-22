"""
Idealista API
Use the idealista.com API
"""
import json
import os
import datetime
import requests
from requests.auth import HTTPBasicAuth
import exceptions


class Client(object):
    def __init__(self, apikey, secret):
        self._apikey = apikey
        self._secret = secret
        self._auth_url = "https://api.idealista.com/oauth/token"
        self._api_base_url = "http://api.idealista.com/3.5/{}/search"
        self.token = None
        self.token_exp = None

    def _get_auth_token(self):
        auth = HTTPBasicAuth(self._apikey, self._secret)
        headers = {'Content-Type': ('application/'
                                    'x-www-form-urlencoded;charset=UTF-8')}
        payload = {'grant_type': 'client_credentials',
                   'scope': 'read'}
        response = requests.post(self._auth_url,
                                 headers=headers,
                                 data=payload,
                                 auth=auth)
        return response

    def _parse_auth(self, response):
        code = response.status_code
        if not code == 200:
            if code == 400 or code == 401:
                resp_dict = json.load(response.text)
                if "error" in resp_dict.keys():
                    msg = "{0}: {1}".format(resp_dict["error"],
                                            resp_dict["error_description"])
                    raise exceptions.AuthFailed(msg)
            else:
                msg = "Authorization Status Code Retruned: {0}".format(code)
                raise exceptions.AuthFailed(msg)
        else:
            return json.loads(response.text)

    def _set_auth_token(self):
        token_dict = self._parse_auth(self._get_auth_token())
        self.token = token_dict['access_token']
        seconds = datetime.timedelta(seconds=token_dict['expires_in'])
        self.token_exp = (datetime.datetime.now() + seconds)

    def _check_token(self):
        if not self.token or not self.token_exp:
            self._set_auth_token()
        elif datetime.datetime.now() > self.token_exp:
            self._set_auth_token()

    def _post(self, country, data):
        self._check_token()
        url = self._api_base_url.format(country)
        headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.post(url,
                                 headers=headers,
                                 data=data)
        return response

    def _parse_post(self, response):
        if not response.status_code == 200:
            msg = json.loads(response.text)['message']
            raise exceptions.SearchFailed(msg)
        else:
            return json.loads(response.text)


if __name__ == '__main__':
    pass
