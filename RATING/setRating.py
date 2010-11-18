#!/usr/bin/python
"""
The MIT License

Copyright (c) 2010 ISKME

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

This client adds a tag to the specified OER Commons resource. 
"""

import sys
sys.path.append('..')

import time
import httplib
import random
import oauth
import urllib
import datetime
import storedauth

# settings for the local test consumer
SERVER = 'www.oercommons.org'
PORT = 80

# fake urls for the test server (matches ones in server.py)
REQUEST_TOKEN_URL = 'http://www.oercommons.org/oauth/request_token'
ACCESS_TOKEN_URL = 'http://www.oercommons.org/oauth/access_token'
AUTHORIZATION_URL = 'http://www.oercommons.org/oauth/authorize'
CALLBACK_URL = 'oob'

RESOURCE_URL = 'http://www.oercommons.org/api/setRating'

stored_auth = storedauth.StoredAuth()

CONSUMER_KEY = stored_auth.getConsumerKey()
CONSUMER_SECRET = stored_auth.getConsumerSecret()
OAUTH_KEY = stored_auth.getAccessKey()
OAUTH_SECRET = stored_auth.getAccessSecret()

# example client using httplib with headers
class SimpleOAuthClient(oauth.OAuthClient):

    def __init__(self, server, port=httplib.HTTP_PORT, request_token_url='', access_token_url='', authorization_url=''):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url

    def fetch_request_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))
        self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header())
        response = self.connection.getresponse().read()
        return oauth.OAuthToken.from_string(response)

    def fetch_access_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))
        self.connection.request(oauth_request.http_method, self.access_token_url, headers=oauth_request.to_header())
        response = self.connection.getresponse()
        return oauth.OAuthToken.from_string(response.read())

    def authorize_token(self, oauth_request):
        # via url
        # -> typically just some okay response
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))
        self.connection.request(oauth_request.http_method, oauth_request.to_url())
        response = self.connection.getresponse()
        return response.read()

    def access_resource(self, oauth_request):
        # via post body
        # -> some protected resources
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))
        headers = {'Content-Type' :'application/x-www-form-urlencoded'}
        self.connection.request('POST', RESOURCE_URL, body=oauth_request.to_postdata(), headers=headers)
        response = self.connection.getresponse()
        return response.read()

def set_rating():

    # setup
    print '** OAuth Python Library Example **'
    client = SimpleOAuthClient(SERVER, PORT, REQUEST_TOKEN_URL, ACCESS_TOKEN_URL, AUTHORIZATION_URL)
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    signature_method_plaintext = oauth.OAuthSignatureMethod_PLAINTEXT()
    signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
    pause()

    token = oauth.OAuthToken(OAUTH_KEY,OAUTH_SECRET)

    # access some protected resources
    print '* Access protected resources ...'
    pause()
    newrating = random.randint(1,5)
    # parameters = {'id': '36354', 'rating': ''}   # test for removing rating
    parameters = {'id': '36354', 'rating': newrating}   # specify id and tag
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_method='POST', http_url=RESOURCE_URL, parameters=parameters)
    oauth_request.sign_request(signature_method_hmac_sha1, consumer, token)
    print 'REQUEST (via post body)'
    print 'parameters: %s' % str(oauth_request.parameters)
    pause()
    params = client.access_resource(oauth_request)
    print 'GOT'
    print 'non-oauth parameters: %s' % params
    pause()

def pause():
    print ''
    time.sleep(1)

if __name__ == '__main__':
    set_rating()
    print 'Done.'

