#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'MasterX2'

vkApp = 00000000 # VK Application ID
scope = 'photos' # Scope
antiGateKey = '123123123123123123' # Antigate API Key
username = 'john.smith@mail.com' # VK Account Email
password = 'password' # VK Account Password

from vkapi import vkApi

vk = vkApi(vkApp, username, password, scope, antiGateKey)

print vk.call('photos.getAll', {'extended': 1})