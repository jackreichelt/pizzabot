from distance import sorensen

PIZZAS = [
  'Australian',
  'BBQ',
  'Biltong Spiced Lamb',
  'c. 1889 Margherita',
  'Capricciosa',
  'Chicken Cordon Bleu',
  'Crust Supreme',
  'Florentine Ricotta',
  'Garlic Prawn',
  'Harissa Hummus Chicken',
  'Hawaiian',
  'Kids Pizza + Juice',
  'Margherita',
  'Meat Deluxe',
  'Mediterranean Lamb',
  'Mexican',
  'Moroccan Lamb',
  'Pancetta',
  'Pepperoni',
  'Peri-Peri',
  'Pesto Chicken Club',
  'Prosciutto',
  'Pulled Pork & Slaw',
  'Quattro Salumi',
  'Sausage Duo',
  'Seafood',
  'Szechuan Chilli Prawn',
  'Tandoori',
  'Truffle Beef Rossini',
  'Vegetarian Supreme',
  'Vietnamese Chilli Chicken',
  'Wagyu Shōga',
  'White Prosciutto',
]

def findPizza(pizzaType):
  lowestScore = 1
  match = ''

  for pizza in PIZZAS:
    score = sorensen(pizza.lower(), pizzaType.lower())
    # print(pizza, score)
    if score < lowestScore:
      lowestScore = score
      match = pizza

  return match
