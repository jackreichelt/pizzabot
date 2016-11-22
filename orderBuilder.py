from os import environ
import requests
from pizzaLoader import createPizzaList

PIZZA_TOKEN = environ['PIZZA_TOKEN']
PIZZA_URL = environ['PIZZA_URL']

pizzas = createPizzaList()

ORDER_TEMPLATE = '''<order type="Object">
   <mobileUuid type="string">77C16387-1BD8-415F-9C53-B0FCC254396C</mobileUuid>
   <userID type="string"></userID>
   <firstName type="string">{}</firstName>
   <lastName type="string">{}</lastName>
   <email type="string">{}</email>
   <mobile type="string">{}</mobile>
   <creditCard type="Object">
      <expiryDate type="Object">
      </expiryDate>
   </creditCard>
   <payment_type type="string">cash</payment_type>
   <acquirementTime type="string">asap</acquirementTime>
   <acquirementMethod type="string">pickup</acquirementMethod>
   <pickupLeadTime type="string">15</pickupLeadTime>
   <deliveryLeadTime type="string">60</deliveryLeadTime>
   <streetNumber type="string"></streetNumber>
   <streetName type="string"></streetName>
   <postcode type="string"></postcode>
   <suburb type="string"></suburb>
   <state type="string"></state>
   <specialInstructions type="string">Built with Messenger Bot</specialInstructions>
   <storeID type="string">4d522da2b386272a08000174</storeID>
   <g type="number">{}</g>
   <orderSource type="string">mobile</orderSource>
   <orderSourceVersion type="string">4.0.1</orderSourceVersion>
   <pifFriendsName type="string"></pifFriendsName>
   <pifFriendsMobile type="string"></pifFriendsMobile>
   <paypalAuthorizationId type="string"></paypalAuthorizationId>
   <paypalAuthorizationCodeForFuturePayments type="string"></paypalAuthorizationCodeForFuturePayments>
   <useSavedPaypalAccount type="boolean">false</useSavedPaypalAccount>
   <tokenise_card_from_mobile type="boolean">false</tokenise_card_from_mobile>
   <token_payment_mobile type="boolean">false</token_payment_mobile>
   <stripe_token type="string"></stripe_token>
   <age_verified type="boolean">false</age_verified>
   <orderItems type="array">
{}   </orderItems>
</order>'''

def createOrderXML(firstName, lastName, email, mobile, itemList):
  pizzaList = []
  totalCost = 0.0
  for pizza in itemList:
    pizzaList.append(pizzas[pizza]['xml'])
    totalCost += pizzas[pizza]['price']

  return ORDER_TEMPLATE.format(firstName, lastName, email, mobile, totalCost, ''.join(pizzaList))

def placeOrder(context):
  orderXML = createOrderXML(context['firstName'], context['lastName'],
                            context['email'], context['mobile'],
                            context['orderItems'])

  # write latest order to debug file
  f = open('order.xml', 'w')
  f.write(orderXML)
  f.close

  resp = requests.post(PIZZA_URL + PIZZA_TOKEN, data=orderXML)
  print('Order response:', resp, resp.content)

# SIDE_TEMPLATE = '''
#       <index{} type="Object">
#          <lineItemPrice type="number">{}</lineItemPrice>
#          <itemType type="string">Side</itemType>
#          <productID type="string">{}</productID>
#          <quantity type="number">{}</quantity>
#       </index{}>
# '''
#
# def createSide(index, price, productid, quantity):
#   return SIDE_TEMPLATE.format(index, price, productid, quantity, index)
