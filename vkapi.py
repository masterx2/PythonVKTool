#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'MasterX2'

from re import findall
from json import loads
from os import remove
from urllib import urlencode, urlopen, urlretrieve
from mechanize import Browser, _http
from antigate import AntiGate

class vkApi(object):
    def __init__(self, appkey, email, password, scope, antiGateKey):
        self.appkey = appkey
        self.email = email
        self.password = password
        self.scope = scope
        self.antiGateKey = antiGateKey

        self.br = Browser()
        self.getToken()


    def getToken(self):
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; U; Android 3.0; \
        ru-RU; Xoom Build/HRI39) AppleWebKit/534.13 KHTML, like Gecko Version/4.0 \
        Safari/534.13')]
        authparams = {
            'client_id': self.appkey,
            'scope': self.scope,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'mobile',
            'v': '5.23',
            'response_type': 'token'
        }

        self.br.open('https://oauth.vk.com/authorize?' + urlencode(authparams))
        self.br.select_form(nr=0)
        self.br.form['email'] = self.email
        self.br.form['pass'] = self.password
        self.br.submit()

        if 'grant_access' in self.br.response().read():
            self.br.select_form(nr=0)
            self.br.submit()
            self.token = self.parseResponse
        else:
            self.token = self.parseResponse

    @property
    def parseResponse(self):
        return dict([x.split('=') for x in findall('\w+=\w+', self.br.geturl())])

    def call(self, method, p):
        strresponse = urlopen(
            'https://api.vk.com/method/'+method+'?'+urlencode(p)+'&access_token='+self.token['access_token']).read()
        ret = loads(strresponse)
        try:
            return ret['response']
        except KeyError:
            if ret['error']['error_code'] == 14:
                print 'Captcha Need'
                urlretrieve(ret['error']['captcha_img'], "cap_file.jpg")
                captcha = AntiGate(self.antiGateKey, 'cap_file.jpg')
                remove('cap_file.jpg')
                p['captcha_sid'] = ret['error']['captcha_sid']
                p['captcha_key'] = captcha
                print 'Another Try...'
                self.call(method, p)
            else:
                print "Unknow Error"
                print ret