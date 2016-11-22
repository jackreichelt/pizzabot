from os import environ
from ast import literal_eval
import requests

FB_APP_TOKEN = environ['FB_APP_TOKEN']

contexts = {}

def getContext(person):
  context = {}
  if person in contexts:
    return contexts[person]
  else:
    resp = requests.get('https://graph.facebook.com/v2.6/{}?fields=first_name,last_name&access_token={}'.format(person, FB_APP_TOKEN)).content
    data = literal_eval(str(resp)[2:-1])
    #TODO: Identify why the data isn't working.
    context['firstName'] = 'Jack' #data['first_name']
    context['lastName'] = 'Reichelt' #data['last_name']
    context['mobile'] = '0432886722'
    context['email'] = 'jack.reichelt@industrieit.com'

    return context

def updateContext(person, newContext):
  contexts[person] = newContext

def clearContext(oldContext):
  preservedElements = [
  'email', # not yet implemented
  'firstName',
  'lastName',
  'lastOrder',
  'mainAddress', # not yet implemented
  'mobile', # not yet implemented
  ]

  newContext = {}
  for item in preservedElements:
    if item in oldContext:
      newContext[item] = oldContext[item]

  return newContext
