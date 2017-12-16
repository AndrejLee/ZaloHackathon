#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:28:21 2017

@author: peterluong
"""

import underthesea as vnltk
from .state import *


class Chatbot(object):
    def __init__(self):
        self._corpus = vnltk.corpus.viet_dict_74K
        self.state = init_state()
        self.prevState = init_state()
        self.lastResponse = ''
    
    def isEnd(self):
        return type(self.state) == type(end_state())
    
    def next_state(self, text):
        self.prevState = self.state
        self.state = self.state.next_State(text, product)
        #A = [token[0] for token in tokens if token[1] == 'A']
        #
        
    def response(self, text):
        text = u"{}".format(text)
        result = ''
        if (self.state.check_relevant(text)):
            self.next_state(text)
            self.lastResponse = self.state.respond(product)
            result = self.lastResponse
        else:
            result = 'Tôi không hiểu ý bạn lắm.' + self.lastResponse
        print(type(self.state))
        print(product)
        return result