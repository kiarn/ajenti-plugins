import logging
import subprocess
import time
from datetime import datetime
import ssl
import socket
from OpenSSL import crypto
from jadi import component

import sys

from aj.api.http import url, HttpPlugin
from aj.auth import authorize
from aj.api.endpoint import endpoint, EndpointError
from .api import checkOnDom

@component(HttpPlugin)
class Handler(HttpPlugin):
    def __init__(self, context):
        self.context = context

    @url(r'/api/lm/check_cert')
    @endpoint(api=True)
    def handle_api_check_cert(self, http_context):
        if http_context.method == 'POST':
            url = http_context.json_body()['url']
            return checkOnDom(*url.split(':'))
            
