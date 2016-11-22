from flask import Flask, request
from contextManager import getContext, updateContext
from messageHandler import handleMessage
from os import environ
import requests

app = Flask(__name__)

FB_APP_TOKEN = environ['FB_APP_TOKEN']

'''
Sends a message to the specified user on FB
'''
def reply(user_id, msg):
  data = {
    'recipient': {'id': user_id},
    'message': {'text': msg}
  }
  # , 'quick_replies':[{'content_type':'text', 'title':'test', 'payload':'test'}]  # quick replies example
  resp = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + FB_APP_TOKEN, json=data)
  print(resp.content)

def checkEnviron():
  requiredEnvironVariables = ['FB_APP_TOKEN', 'PIZZA_TOKEN', 'WIT_TOKEN']
  missingEnvironVars = [x for x in requiredEnvironVariables if x not in environ]

  if len(missingEnvironVars) > 0:
    print('Missing environment variables:', ', '.join(missingEnvironVars))
    exit(-1)

@app.route('/', methods=['POST'])
def handle_incoming_messages():
  data = request.json
  # print('data received', data)

  for entry in data['entry']:
      for msg in entry['messaging']:
        sender = msg['sender']['id']
        if 'message' in msg and sender != '580959678695274': # this is the bot's ID.
          if 'text' in msg['message']:
            message = msg['message']['text']
            context = getContext(sender)

            messageResponse = handleMessage(sender, message, context)

            updateContext(sender, messageResponse['context'])
            reply(sender, messageResponse['reply'])

  return 'ok'

@app.route('/', methods=['GET'])
def handle_verification():
  return request.args['hub.challenge']

@app.route('/<path:path>')
def catch_all(path):
  print('A weird request has occured! It was pointed at /{}'.format(path))
  return 'ok'

if __name__ == '__main__':
  checkEnviron()
  app.run(debug=True)
