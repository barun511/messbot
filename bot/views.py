import json
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic


def is_token_valid(token):
    return token == "recognitioncode821potato"

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
                    print(message)
        return HttpResponse()
