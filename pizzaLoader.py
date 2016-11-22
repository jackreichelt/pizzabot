import xml.etree.ElementTree as ET
import requests
from ingredientLoader import loadIngredients

ingredients = loadIngredients()

LARGE_SIZE = '4d522df4b386272a0800073c'
MED_SIZE = '4d522df4b386272a08000735'

PIZZA_TOKEN = 'JackIsCool374'
PIZZA_TEMPLATE = '''      <item type="Object">
         <lineItemPrice type="number">{}</lineItemPrice>
         <itemType type="string">Pizza</itemType>
         <productID type="string">{}</productID>
         <quantity type="number">{}</quantity>
         <sizeID type="string">{}</sizeID>
         <baseID type="string">{}</baseID>
         <doughID type="string">{}</doughID>
         <itemIngredients type="array">
{}         </itemIngredients>
      </item>
'''

def createPizza(price, productID, quantity, size, base, dough, ingredientsList):
  return PIZZA_TEMPLATE.format(price, productID, quantity, size, base, dough, ''.join(ingredientsList))

def createPizzaList():
  pizzas = {}

  xml = requests.get('https://staging.crusthq.com.au/api/pizzas/' + PIZZA_TOKEN).content
  root = ET.fromstring(xml)

  for pizza in root.findall('pizza'):
    name = pizza.find('name').text

    price = 0
    prices = pizza.find('prices')
    price = float(prices.find('price').text)
    size = prices.find('price').attrib['sizeID']

    productID = pizza.attrib['id']

    quantity = 1 # change to read a quantity

    base = pizza.find('base').attrib['id']

    dough = ''
    doughList = pizza.find('doughs')
    for doughItem in doughList.findall('dough'):
      if doughItem.find('is_base').text == 'true':
        dough = doughItem.attrib['id']

    ingredientsList = []
    for ingredientItem in pizza.find('ingredients').findall('ingredient'):
      if ingredientItem.find('is_base').text == 'true':
        ingredientsList.append(ingredients[ingredientItem.attrib['id']])

    pizzas[name] = {'xml': createPizza(price, productID, quantity, size, base, dough, ingredientsList), 'price':price}

  return pizzas
