import json,requests
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic

valid_menu_options = ["lunch","dinner","breakfast","snacks"]

def is_token_valid(token):
    return token == "recognitioncode821potato"

class Message:
    def __init__(self, userid, messagetext):
        self.userid = userid
        self.messagetext = messagetext

class FacebookBotView(generic.View):

    def get(self, request, *args, **kwargs):
        if is_token_valid(self.request.GET['hub.verify_token']):
            return HttpResponse(request.GET['hub.challenge'])

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    messageobject = Message(message['sender']['id'],message['message']['text'])
                    messageobject.messagetext = handle_message(messageobject) # this is cool, swaps text but keeps id
                    send_facebook_message(messageobject)
                    
        return HttpResponse()

def send_facebook_message(message_object):
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=EAADr9sJWBYkBAOuQsnZAvZA0nIrZCje4jtKAOVl7GoeDQZANpHnIDF088JTxnRgUyg2ZCIOZCwxcg02o1hac5OcRvS81rICyAJol4aeYsyrANv9PfC5YwL2VM0gyFY1pfaBVyZAxD5Tv2PN9lFP4k8uTZBCa7cd53JT23IIlhqrbD9HZCUPdX7nki"
    message = json.dumps({"recipient":{"id":message_object.userid}, "message" : {"text": message_object.messagetext}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=message)
    print(status.json())


def handle_message(message_object): # Expects a message object
    message_tokens = message_object.messagetext.split()

    if message_tokens[0] == "menu":
        if message_tokens[1] == "breakfast":
            return "You asked for the breakfast menu"
        elif message_tokens[1] == "lunch":
            return "You asked for the lunch menu"
        elif message_tokens[1] == "snacks" or message_tokens[1] == "snack":
            return "You asked for the snacks menu"
        elif message_tokens[1] == "dinner":
            return "You asked for the dinner menu"
