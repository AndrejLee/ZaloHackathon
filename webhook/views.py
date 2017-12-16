# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from .serializers import WebHookSerializer, UploadFileForm
from main.serializers import MessageSerializer
from main.chatbot import Chatbot
from hashlib import sha256
import requests
from chatbot.settings import BASE_DIR
from .retrieve_im import chatbot_retrieve
import os

base_path = os.path.join(BASE_DIR)

my_chat_bot = Chatbot()


class WebHookView(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request, format=None):
        image_msg = ""
        data = request.query_params
        if 'href' in data.keys():
            image_msg = upload_file(request)
            del data['href']
            del data['thumb']
        serializer = WebHookSerializer(data=data)
        if serializer.is_valid():
            web_hook = serializer.save()
            # user_respond
            msg = web_hook.message
            # chatbot_respond
            if image_msg:
                respond_text = my_chat_bot.response(text=image_msg)
            else:
                respond_text = my_chat_bot.response(text=msg)
            # send message to user
            if respond_text:
                chatbot_respond(respond_text, web_hook)
            respond_serializer = MessageSerializer(data={
                "webhook": web_hook.id,
                "respond": respond_text
            })
            # save respond_message to database
            if respond_serializer.is_valid(raise_exception=True):
                respond_serializer.save()
            return Response({"message": "Received and saved"}, 200)
        else:
            return Response({"message": "Error", "errors": serializer.errors}, 400)


def chatbot_respond(message, webhook_object):
    secret_key = "75CPjjUB9MbW5Ls6yBAE"
    data_string = "{\"uid\":" + str(webhook_object.fromuid) + ",\"message\":\"" + str(message) + "\"}"
    mac_string = bytes(str(webhook_object.oaid) + data_string + str(webhook_object.timestamp) + secret_key, 'utf-8')
    request_body = {
        "oaid": webhook_object.oaid,
        "data": data_string,
        "timestamp": webhook_object.timestamp,
        "mac": sha256(mac_string).hexdigest()
    }
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json"
    }
    url = "https://openapi.zaloapp.com/oa/v1/sendmessage/text"
    response = requests.post(url, headers=headers, data=request_body)
    return response.text


def test_chatbot_respond():
    import pdb
    pdb.set_trace()
    secret_key = "75CPjjUB9MbW5Ls6yBAE"
    data = {
        "uid": 3419256448411196340,
        "message": "adsd"
    }
    data_string = "{\"uid\":3419256448411196340,\"message\":\"adsd\"}"
    mac_string = bytes("13270656314381663" + str(data_string) + str(1513437582118) + secret_key, 'utf-8')
    request_body = {
        "oaid": 13270656314381663,
        "data": data_string,
        "timestamp": 1513437582118,
        "mac": sha256(mac_string).hexdigest()
    }
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json"
    }
    url = "https://openapi.zaloapp.com/oa/v1/sendmessage/text"
    response = requests.post(url, headers=headers, data=request_body)
    return response.text


def upload_file(request):
    if 'href' in request.query_params:
        image = requests.get(request.query_params['href'], allow_redirects=True)
        image_path = '{}/images/user_image.png'.format(base_path)
        open(image_path, 'wb').write(image.content)

        # return info of image
        response_message = chatbot_retrieve(image_path)
        return response_message



