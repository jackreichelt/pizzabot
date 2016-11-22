import xml.etree.ElementTree as ET
import requests

PIZZA_TOKEN = 'JackIsCool374'
INGREDIENT_TEMPLATE = '''            <itemIngredients type="Object">
               <ingredientAmount type="number">{}</ingredientAmount>
               <ingredientID type="string">{}</ingredientID>
            </itemIngredients>
'''

def createIngredient(quantity, ingredientid):
  return INGREDIENT_TEMPLATE.format(quantity, ingredientid)

def loadIngredients():
  ingredients = {}

  xml = requests.get('https://staging.crusthq.com.au/api/ingredients/' + PIZZA_TOKEN).content
  root = ET.fromstring(xml)
  
  for ingredient in root.findall('ingredient'):
    ingredientID = ingredient.attrib['id']
    ingredients[ingredientID] = INGREDIENT_TEMPLATE.format(1, ingredientID)

  return ingredients
