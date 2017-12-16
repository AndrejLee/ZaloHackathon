#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 12:34:43 2017

@author: peterluong
"""

from chatbot import Chatbot

myChatbot = Chatbot()

while(not myChatbot.isEnd()):
    sent = input()
    print(myChatbot.response(sent))