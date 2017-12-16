#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 12:53:01 2017

@author: peterluong
"""
import underthesea as vnltk
import json
import os
from chatbot import settings

base_path = os.path.join(settings.BASE_DIR)

with open('{}/main/zdata/final-rel-path.json'.format(base_path)) as f:
    database = json.load(f)

product = {}
def object_parse(N):
    result = []
    for each in N:
        if each in ['cáp']:
            result.append('cap-dien-thoai')
        if each in ['tai nghe']:
            result.append('tai-nghe')
        if each in ['điện thoại', 'điện thoại di động']:
            result.append('Điện thoại')
        if each in ['phụ kiện']:
            result.extend(['phu-kien','phu-kien-chinh-hang','phu-kien-khac'])
        if each in ['usb']:
            result.append('usb')
        if each in ['laptop', 'máy tính']:
            result.append('Laptop')
        if each in ['chuột', 'chuột máy tính']:
            result.append('chuot-may-tinh')
        if each in ['sạc', 'sạc điện thoại']:
            result.append('sac-dtdd')
        if each in ['thẻ nhớ']:
            result.append('the-nho-dien-thoai')
    return result

def convert2num(s):
    if s == 'triệu':
        return '000000'
    if s == ' ngàn':
        return '000'
    if s == 'trăm':
        return '00'
    if s == 'mươi':
        return '0'
    try:
        float(s)
        return s
    except ValueError:
        return ''
        
    return ''
    
def price_parse(tokens):
    result = ''
    print(tokens)
    for each in tokens:
        if each[1] == 'M':
            result = result + convert2num(each[0])
    return result

def branch_parse(tokens):
    result = ''
    for each in tokens:
        if each[3] != 'O':
            result = result + ' ' + each[0]
    return result

class State(object):
    def __init__(self):
        self.response = ''
        
    def next_State(self, text, product):
        result = State()
        return result
    
    def respond(self, product):
        return self.response;
    
    def check_relevant(self, text):
        print('not check relevant')
        return True
    
    def specify_respond(self, product):
        return self.response;
    
class init_state(State):
    def __init__(self):
        self.response = ''
    def next_State(self, text, product):
        return welcome_state()

class welcome_state(State):
    def __init__(self):
        self.response = 'Xin chào. tôi có thể giúp gì cho bạn'
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] == 'N']
        product['category'] = object_parse(N)
        product['price'] = price_parse(tokens)
        product['branch'] = branch_parse(tokens)
        
        if product['price'] != '' and product['branch'] != '':
            return completeInfo_state()
        if product['price'] != '' and product['branch'] == '':
            return knowCP_state()
        if product['price'] == '' and product['branch'] != '':
            return knowCB_state()
        
        return knowCategory_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] == 'N']
        temp = object_parse(N)
        return temp != []
    
class knowCategory_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua với giá khoảng bao nhiêu?'
        
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        product['price'] = price_parse(tokens)
        if 'Điện thoại' not in product['category'] and 'Laptop' not in product['category']:
            return completeInfo_state()
        return knowCP_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        price = price_parse(tokens)
        return price != ''

class knowCB_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua với giá khoảng bao nhiêu?'
    
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        product['price'] = price_parse(tokens)
        return completeInfo_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        price = price_parse(tokens)
        return price != ''
    
class knowCP_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua sản phẩm của hãng nào?'
    
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        product['branch'] = branch_parse(tokens)
        return completeInfo_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        branch = branch_parse(tokens)
        return branch != ''

class completeInfo_state(State):
    def __init__(self):
        self.response = 'Bạn có thể tham khảo các sản phẩm sau'
        self.proposal_items = []
        for each in database:
            if (each['category'] in product['category']):
                self.proposal_items.append(each)
        self.current = 0
    
    def isBought(self, tokens):
        return True
    
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        if (self.isBought(tokens)):
            return bought_state()
        if (self.isNextItem()):
            
            return self
        return  end_state()
    
    def respond(self, product):
        for each in self.proposal_items[self.current:5]:
            print(each.keys())
            self.response = self.response + '\n' + each['imgUrl']
        return self.response

class bought_state(State):
    def __init__(self):
        self.response = 'Cảm ơn bạn đã mua hàng của chúng tôi. Bạn muốn mua gì khác không?'
    
    def isContinue(self, tokens):
        return False
    
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        if (self.isContinue(tokens)):
            return continue_state()
        else:
            return end_state()
        
class end_state(State):
    def __init__(self):
        self.response = 'Hẹn gặp lại bạn trong những lần mua sắm tới'
    
    def next_State(self, text, product):
        return end_state()
    
class continue_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua loại sản phẩm nào?'
    
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] == 'N']
        product['category'] = object_parse(N)
        product['price'] = price_parse(tokens)
        product['branch'] = branch_parse(tokens)
        
        if product['price'] != '' and product['branch'] != '':
            return completeInfo_state()
        if product['price'] != '' and product['branch'] == '':
            return knowCP_state()
        if product['price'] == '' and product['branch'] != '':
            return knowCB_state()
        
        return knowCategory_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] == 'N']
        temp = object_parse(N)
        return temp != []