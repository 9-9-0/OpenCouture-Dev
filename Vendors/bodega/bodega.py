import requests
from requests.utils import dict_from_cookiejar
from bs4 import BeautifulSoup
from selenium import webdriver
import code
import webbrowser
import re

#Functions used for testing, eventually incorporate into unit-tests
def savePage( response, filename ):
    output = open(filename, 'wb')
    for chunk in response.iter_content(100000):
        output.write(chunk)
def exitConf():
    closeSession = False
    while (closeSession == False):
        input = raw_input('Press E to close session: ')
        if (input == 'E'):
            closeSession = True

# Presets 
# Move these members to a profile class eventually 
URL_vendor_url  = 'http://shop.bdgastore.com/'
URL_direct_link = 'http://shop.bdgastore.com/collections/footwear/products/y-3-pureboost-zg'
user_size = 8

#################
## Main Script ##
#################

user_session = requests.Session()
session_get  = user_session.get(URL_direct_link)
print 'Status of requests.get: ' + str(session_get.status_code)
savePage(session_get, 'test2.html')

prod_soup = BeautifulSoup(session_get.content, "lxml")
#Check that the lxml parser works for html
#Look to use SoupStrainer to improve parsing efficiency

ResultSet = prod_soup.find_all('form', {'id' : 'qv-form'})
ResultSetString = unicode.join(u'\n',map(unicode,ResultSet))
ResultSoup = BeautifulSoup(ResultSetString, "lxml")
#print ResultSoup.prettify()
with open('bodegaForm.html', 'wb') as bodegaFormFile:
    bodegaFormFile.write(ResultSoup.prettify())

#select: name="id" value=22348567876 (11.5)
#input:  id="key" name="properties[bot-key]" type="hidden" value="6402243972

#Note: posted data might not be correct
post_data = { 'id':'22348567876', 'properties[bot-key]':'6402243972' }
add_to_cart_js = 'http://shop.bdgastore.com/cart/add.js'
session_post = user_session.post(url=add_to_cart_js, data=post_data)

print str(session_post.status_code)

session_get  = user_session.get('http://shop.bdgastore.com/')
print str(user_session.cookies) + '\n'

cookies = dict_from_cookiejar(user_session.cookies)
print cookies

driver = webdriver.Firefox()
driver.add_cookie(cookies)
driver.add_cookie({'path':'/'})
driver.get('http://shop.bdgastore.com/cart')
#So the posted data gets accepted...but why doesn't the item show in the cart after the cookies get imported?
#Possible Reason: cart_sig cookie is empty


# Data of interest:
#  <select class="" id="product-select" name="id">  <-- Corresponds to the value that will be sent over with add.js
#  <input id="key" name="properties[bot-key]" type="hidden" value="6402243972"/>  <-- Value probably related to a Database Entry

#for size in prod_soup.findAll('option'):
#    if size.parent.name == 'select':
#        print size
#        print size['value']

#print '\n'

#arr = prod_soup.findAll('option')
#print arr[0]
#print arr[1]
#print type(arr[0])

#post_data = {
#http://shop.bdgastore.com/cart/add.js

#Uncomment ln 3 and 43 to launch into interpreter
#code.interact(local=locals())
