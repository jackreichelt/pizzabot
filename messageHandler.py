from pizzas import findPizza
from witConnector import witMessage
from orderBuilder import placeOrder
from contextManager import clearContext

def repeatLastOrder(context):
  if 'lastOrder' not in context:
    reply = '''
      You need to have placed an order before to use the repeat feature.
      '''
    return {'context': context,
            'reply'  : reply}

  context['orderItems'] = context['lastOrder']
  context['repeating'] = True

  reply = reply = '''
    We're going to repeat your last order. Here's what it was:
  {}
Shall we go ahead and place it?
    '''.format('\n  '.join(context['orderItems']))
  return {'context': context,
          'reply'  : reply}

def helpMessage(context, witResponse):
  reply = '''
    Hi there. Looks like you're trying something I don't understand. This
    prototype can only order default pizzas off the menu. Currently it's
    restricted in several ways. It always sends as Jack, to the same
    location, and doesn't allow sides or customisation. If you're stuck,
    try typing something like, "I'd like to order a margharita."
    '''
  return {'context': context,
          'reply'  : reply}

def addToOrder(context, witResponse):
  if 'pizza_type' not in witResponse['entities']:
    return helpMessage(context, witResponse)

  for pizza in witResponse['entities']['pizza_type']:
    pizzaType = pizza['value']
    pizza = findPizza(pizzaType)
    if 'orderItems' in context:
      context['orderItems'].append(pizza)
    else:
      context['orderItems'] = [pizza]

  if len(witResponse['entities']['pizza_type']) == 1:
    reply = '''
  I've added a {} pizza to your order. Here's your current cart:
  {}
Would you like to place your order?
      '''.format(pizza, '\n  '.join(context['orderItems']))
  else:
    reply = '''
  I've added those pizzas to your order. Here's your current cart:
  {}
Would you like to place your order?
      '''.format('\n  '.join(context['orderItems']))

  return {'context': context,
          'reply'  : reply}

def confirmOrder(context, witResponse):
  if 'orderItems' not in context:
    # This clause should never run if repeating an order.
    reply = '''
      You need to order something first.
      '''
    return {'context': context,
            'reply'  : reply}

  context['lastOrder'] = context['orderItems']
  placeOrder(context)

  context = clearContext(context)
  reply = '''
Your order has been placed.
  '''

  return {'context': context,
          'reply'  : reply}

def approveRepeat(context, witResponse): # Depricated
  # This function is synonymous with confirmOrder.
  # It's separated for clarity of purpose when repeating.
  return confirmOrder(context, witResponse)

def rejectRepeat(context, witResponse):
  context['orderItems'] = []
  if 'repeating' in context: context.pop('repeating')
  reply = '''
  No worries. If you'd like to order something else,
just add pizzas to your order like normal.
  '''
  return {'context': context,
          'reply'  : reply}

def removePizza(context, witResponse):
  if 'orderItems' not in context:
    reply = '''
      You need to order something first.
      '''
    return {'context': context,
            'reply'  : reply}

  if 'pizza_type' not in witResponse['entities']:
    return helpMessage(context, witResponse)

  for pizza in witResponse['entities']['pizza_type']:
    pizzaType = pizza['value']
    pizza = findPizza(pizzaType)
    if pizza in context['orderItems']:
      context['orderItems'].remove(pizza)
    else:
      reply = '''
        You didn't have any pizzas of that type.
        '''
      return {'context': context,
              'reply'  : reply}

  if len(context['orderItems']) == 0:
    reply = '''
I've removed that from your cart. It's now empty.
'''
  elif len(witResponse['entities']['pizza_type']) == 1:
    reply = '''
  I've removed that pizza from your order. Here's your current cart:
  {}
Would you like to place your order?
      '''.format('\n  '.join(context['orderItems']))
  else:
    reply = '''
  I've removed those pizzas from your order. Here's your current cart:
  {}
Would you like to place your order?
      '''.format('\n  '.join(context['orderItems']))

  print('New context:', context)
  return {'context': context,
          'reply'  : reply}

def handleMessage(sender, message, context):
  # define a function for each special message and include them in this dictionary
  specialMessages = {
    '🍕': repeatLastOrder,
  }

  intents = {
    'help'          : helpMessage,
    'order'         : addToOrder,
    'confirmOrder'  : confirmOrder,
    'approveRepeat' : confirmOrder, # Depricated
    'rejectRepeat'  : rejectRepeat,
    'removePizza'   : removePizza,
  }

  if message.lower() in specialMessages:
    return specialMessages[message](context)

  witResponse = witMessage(sender, message, context)

  intent = witResponse['entities']['intent'][0]['value'] if 'intent' in witResponse['entities'] else 'help'

  return intents[intent](context, witResponse)
