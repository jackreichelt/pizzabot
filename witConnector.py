from os import environ
from wit import Wit

WIT_TOKEN = environ['WIT_TOKEN']

def send(request, response):
  print('Sending to user...', response['text'])
def getMessage(request):
  print('Received from user...', request['text'])

actions = {
  'send': send,
  'getMessage': getMessage
}

witClient = Wit(access_token=WIT_TOKEN, actions=actions)

def witMessage(sender, message, context):
  return witClient.converse(sender, message, context)
