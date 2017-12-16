#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 12:53:01 2017

@author: peterluong
"""
import underthesea as vnltk
import json
import random

with open('zdata/final-rel-path.json') as f:
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


def num_process(word):
    num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    mul = {'k': 1000, 'm': 1000000}

    cs = list(word)
    if any(c not in num + list(mul.keys()) for c in cs):
        return None
    tmp1 = []
    i = 0
    for c in cs:
        if c in num:
            tmp1.append(c)
        else:
            break
        i += 1
    tmp2 = []
    for c in cs[i:]:
        if c in mul:
            tmp2.append(c)
        else:
            return None
    res = int(''.join(tmp1))
    cof = 1
    for tmp in tmp2:
        cof *= mul[tmp]
    return res * cof

def convert_number(sent):
    num_words = {'không': 0, 'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5, 'sáu': 6,
                 'bảy': 7, 'tám': 8, 'chín': 9, 'mười': 10}
    mul_words = {'tỉ': 1000000000, 'tỷ': 1000000000, 'triệu': 1000000, 'm': 1000000, 'trăm': 100,
                 'nghìn': 1000, 'k': 1000, 'chục': 10, 'mươi': 10}
    add_words = {'lẻ': 0., 'rưỡi': 0.5}
    req_words = list(num_words.keys()) + list(mul_words.keys()) + list(add_words.keys())

    req_nums = list(num_words.keys()) + ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    words = sent.split(' ')

    i = -1
    numlists = []

    while i < len(words):
        numlist = []
        w = words[i]

        if any(n in w for n in req_nums):
            while w in req_words or any(n in w for n in req_nums):
                numlist.append((w, i))
                i += 1
                if i < len(words):
                    w = words[i]
                else:
                    break
        if numlist != []:
            numlists.append(numlist)

        i += 1

    res = []
    for numlist in numlists[-1::-1]:
        num = 0
        n_words = [n[0] for n in numlist]
        idx = (numlist[0][1], numlist[-1][1])

        i = 0
        while(i < len(n_words)):
            w = n_words[i]
            tmp = 0
            if any(n in w for n in req_nums):
                if w in num_words.keys():
                    tmp += num_words[w]
                else:
                    tmp1 = num_process(w)
                    if tmp1 != None:
                        tmp = tmp1
                    else:
                        break
                while i < len(n_words) - 1 and (n_words[i+1] in mul_words.keys() or n_words[i+1] in add_words.keys()):
                    if n_words[i+1] in mul_words.keys():
                        tmp *= mul_words[n_words[i+1]]
                    elif n_words[i+1] in add_words.keys():
                        tmp2 = tmp
                        x = 0
                        while tmp2 % 10 == 0:
                            tmp2 /= 10
                            x += 1
                        x = x // 3
                        tmp += int(add_words[n_words[i+1]] * 10**(x*3))
                    i += 1




            num += tmp
            i += 1
        if num != 0:
            res.append(num)

    if res == []:
        return ''
    return str(max(res))
    
def price_parse(text):
    return convert_number(text)

def branch_parse(tokens):
    result = ''
    for each in tokens:
        if each[3] != 'O':
            result = result + ' ' + each[0]
    return result

def check_endProcess(text):
    return text in ['tôi không muốn mua nữa', 'tôi không mua nữa', 'kết thúc việc mua sắm', 'thôi không mua nữa', 'không mua nữa', 'không có', 'không mua']

def check_suggest(text):
    tokens = vnltk.word_sent(text)
    return ('giới thiệu' in tokens) or ('gợi' in tokens and 'ý' in tokens)

class State(object):
    def __init__(self):
        self.response = ''
        
    def next_State(self, text, product):
        result = State()
        return result
    
    def respond(self, product):
        return {'text':self.response, 'multimedia':[]}
    
    def check_relevant(self, text):
        return True
    
    def specify_respond(self, product):
        return {'text':self.response, 'multimedia':[]}
    
class init_state(State):
    def __init__(self):
        self.response = ''
        
    def checkWelcome(tokens):
        return 'chào' in [t[0] for t in tokens]
    
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1]  in ['N','M']]
        product['category'] = object_parse(N)
        product['price'] = price_parse(text)
        product['branch'] = branch_parse(tokens)
        
        if (product['category'] != []):
            if product['price'] != '' and product['branch'] != '':
                return completeInfo_state()
            if product['price'] != '' and product['branch'] == '':
                return knowCP_state()
            if product['price'] == '' and product['branch'] != '':
                return knowCB_state()
        
        return welcome_state()

class welcome_state(State):
    def __init__(self):
        self.response = 'tôi có thể giúp gì cho bạn?'
    def next_State(self, text, product):
        if (check_endProcess(text)):
            return end_state()
        if (check_suggest(text)):
            return suggest_state()
        
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1]  in ['N','M']]
        product['category'] = object_parse(N)
        product['price'] = price_parse(text)
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
        N = [token[0] for token in tokens if token[1] in ['N', 'M']]
        temp = object_parse(N)
        return temp != [] or check_endProcess(text) or check_suggest(text)
    
class knowCategory_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua với giá khoảng bao nhiêu?'
        
    def next_State(self, text, product):
        if (check_endProcess(text)):
            return end_state()
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] in ['N', 'M']]
        new_category = object_parse(N)
        product['price'] = price_parse(text)
        product['branch'] = branch_parse(tokens)
        if (new_category != [] and new_category != product['category']):
            product['category'] = new_category
            if product['price'] != '' and product['branch'] != '':
                return completeInfo_state()
            if product['price'] != '' and product['branch'] == '':
                return knowCP_state()
            if product['price'] == '' and product['branch'] != '':
                return knowCB_state()
            return knowCategory_state()
        
        if 'Điện thoại' not in product['category'] and 'Laptop' not in product['category']:
            return completeInfo_state()
        
        if product['price'] != '' and product['branch'] == '':
            return knowCP_state()
        
        if product['price'] == '' and product['branch'] != '':
            return knowCB_state()
        
        if product['price'] != '' and product['branch'] != '':
                return completeInfo_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] in ['N', 'M']]
        new_category =  object_parse(N)
        price = price_parse(text)
        branch = branch_parse(tokens)
        return price != '' or new_category != [] or branch != '' or check_endProcess(text)
    
class knowCB_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua với giá khoảng bao nhiêu?'
    
    def next_State(self, text, product):
        if (check_endProcess(text)):
            return end_state()
        tokens = vnltk.ner(text)
        product['price'] = price_parse(text)
        return completeInfo_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        price = price_parse(text)
        return price != '' or check_endProcess(text)
    
    def specify_respond(self, product):
        return {'text':'Bạn muốn mua ' + product['category'][0] + ' với giá khoảng bao nhiêu?', 'multimedia':[]}
        
class knowCP_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua sản phẩm của hãng nào?'
    
    def next_State(self, text, product):
        if (check_endProcess(text)):
            return end_state()
        tokens = vnltk.ner(text)
        product['branch'] = branch_parse(tokens)
        return completeInfo_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        branch = branch_parse(tokens)
        return branch != '' or check_endProcess(text)
    
    def specify_respond(self, product):
        return {'text':'Bạn muốn mua ' + product['category'][0] + ' của hãng nào?','multimedia':[]}

class completeInfo_state(State):
    def __init__(self):
        self.response = 'Bạn cần tìm ' + product['category'][0] +  ' giá ' + product['price'] + '. Bạn có thể tham khảo sản phẩm '
        self.proposal_items = []
        for each in database:
            if (each['category'] in product['category']):
                self.proposal_items.append(each)
        self.current = 0
        self.current_product = {}
        
    def question_parse(self, text):
        tokens = vnltk.word_sent(text)
        result = []
        if '?' in tokens:
            if 'gì' in tokens or 'bao nhiêu' in tokens or 'thế nào' in tokens:
                if 'giá' in tokens or 'giá cả' in tokens:
                    result.append('price')
                if 'tên' in tokens:
                    result.append('name')
                result.append('null')
        return result
    
    def isBought(self, tokens):
        text = [t[0] for t in tokens]
        return 'mua' in text or 'chọn' in text
    
    def isNextItem(self, text):
        tokens = vnltk.word_sent(text)
        return 'khác' in tokens or text in ['tôi không thích cái này', 'không mua', 'không muốn cái này', 'không thích cái này', 'bỏ qua cái này', 'bỏ qua']
    
    def next_State(self, text, product):
        if (check_endProcess(text)):
            return end_state()
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] in ['N', 'M']]
        new_category =  object_parse(N)
        if (new_category != [] and new_category != product['category']):
            product['category'] = new_category
            return knowCategory_state()
        
        querry = self.question_parse(text)
        if (querry != []):
            return ask_state(querry, self.current_product)
        
        if (self.isNextItem(text)):
            self.current += 5
            return self
        
        if (self.isBought(tokens)):
            return bought_state()
        
        return  end_state()
    
    def respond(self, product):
        multimedia = []
        self.current_product = self.proposal_items[self.current]
        multimedia.append(self.current_product['imgUrl'])
        return {'text':self.response + self.current_product['name'], 'multimedia':multimedia}
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        return (check_endProcess(text) or self.isBought(tokens) or self.isNextItem(text)) or self.question_parse(text) != []
    
    def specify_respond(self, product):
        multimedia = []
        self.current_product = self.proposal_items[self.current]
        multimedia.append(self.current_product['imgUrl'])
        return {'text': 'Bạn có thể tham khảo mẫu ' + product['category'][0] + ' ' + self.current_product['name'], 'multimedia':multimedia}
        
class bought_state(State):
    def __init__(self):
        self.response = 'Đơn hàn của bạn đã được ghi nhận. Cảm ơn bạn đã mua sắm của chúng tôi. Bạn muốn mua gì khác không?'
    
    def isContinue(self, text):
        return text in ['có', 'có tôi muốn mua nữa', 'có tôi mua nữa', 'mua nữa']
    
    def isStop(self, text):
        return text in ['không', 'thôi', 'khỏi', 'thôi khỏi', 'thôi không']
    
    def next_State(self, text, product):
        if (check_endProcess(text) or self.isStop(text)):
            return end_state()
        if (self.isContinue(text)):
            return continue_state()
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1]  in ['N','M']]
        product['category'] = object_parse(N)
        product['price'] = price_parse(text)
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
        N = [token[0] for token in tokens if token[1] in ['N', 'M']]
        temp = object_parse(N)
        return temp != [] or check_endProcess(text) or self.isContinue(text) or self.isStop(text)
    
class end_state(State):
    def __init__(self):
        self.response = 'Hẹn gặp lại bạn trong những lần mua sắm tới'
    
    def next_State(self, text, product):
        return init_state()
    
class continue_state(State):
    def __init__(self):
        self.response = 'Bạn muốn mua loại sản phẩm nào?'
    
    def next_State(self, text, product):
        tokens = vnltk.ner(text)
        N = [token[0] for token in tokens if token[1] == 'N']
        product['category'] = object_parse(N)
        product['price'] = price_parse(text)
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

class ask_state(State):
    def __init__(self, querry, current_product):
        self.response = ''
        self.current_product = current_product
        try:
            self.response = current_product[querry[0]]
        except KeyError:
            self.response = 'Thông tin này hiện bị thiếu. Bạn hãy liên hệ số điện thoại 0983118326 để biết thêm chi tiết'
    
    def question_parse(self, text):
        tokens = vnltk.word_sent(text)
        result = []
        if '?' in tokens:
            if 'gì' in tokens or 'bao nhiêu' in tokens or 'thế nào' in tokens:
                if 'giá' in tokens or 'giá cả' in tokens:
                    result.append('price')
                if 'tên' in tokens:
                    result.append('name')
                result.append('null')
        return result
    
    def isBought(self, tokens):
        text = [t[0] for t in tokens]
        return 'mua' in text or 'chọn' in text
    
    def isNextItem(self, tokens):
        return 'khác' in [t[0] for t in tokens]
    
    def next_State(self, text, product):
        if (check_endProcess(text)):
            return end_state()
        tokens = vnltk.ner(text)
        querry = self.question_parse(text)
        if (querry != []):
            return ask_state(querry, self.current_product)
        
        if (self.isNextItem(tokens)):
            return completeInfo_state()
        
        if (self.isBought(tokens)):
            return bought_state()
        
        return  end_state()
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        return (check_endProcess(text) or self.isBought(tokens) or self.isNextItem(tokens)) or self.question_parse(text) != []
    
class suggest_state(State):
    def __init__(self):
        id = random.randint(1,2000)
        self.current_product = database[id]
        self.response = self.current_product['name'] + ' đang khuyến mãi. Bạn có muốn mua không?'
        
    def question_parse(self, text):
        tokens = vnltk.word_sent(text)
        result = []
        if '?' in tokens:
            if 'gì' in tokens or 'bao nhiêu' in tokens or 'thế nào' in tokens:
                if 'giá' in tokens or 'giá cả' in tokens:
                    result.append('price')
                if 'tên' in tokens:
                    result.append('name')
                result.append('null')
        return result
    
    def isBought(self, tokens):
        text = [t[0] for t in tokens]
        return 'mua' in text or 'chọn' in text or 'có' in text
    
    def isNextItem(self, tokens):
        return 'khác' in [t[0] for t in tokens]
    
    def next_State(self, text, product):
        if (check_endProcess(text)):
            return end_state()
        tokens = vnltk.ner(text)
        querry = self.question_parse(text)
        if (querry != []):
            return ask_state(querry, self.current_product)
        
        if (self.isNextItem(tokens)):
            return suggest_state()
        
        if (self.isBought(tokens)):
            return bought_state()
        
        return  end_state()
    
    def respond(self, product):
        multimedia = []
        print(self.current_product)
        multimedia.append(self.current_product['imgUrl'])
        return {'text':self.response, 'multimedia':multimedia}
    
    def check_relevant(self, text):
        tokens = vnltk.ner(text)
        return check_endProcess(text) or self.isBought(tokens) or self.isNextItem(tokens) or self.question_parse(text) != []
    
    def specify_respond(self, product):
        multimedia = []
        print(self.current_product)
        multimedia.append(self.current_product['imgUrl'])
        return {'text':self.response, 'multimedia':multimedia}