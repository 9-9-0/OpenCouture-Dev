import requests
from requests.utils import dict_from_cookiejar
from bs4 import BeautifulSoup
from selenium import webdriver
import code
import webbrowser
import re
import mechanize

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

#################
## Main Script ##
#################
class bodegaREQ():
    def __init__(self):
        self.URL_vendor_url  = 'http://shop.bdgastore.com/'
        self.URL_direct_link = 'http://shop.bdgastore.com/collections/footwear/products/y-3-pureboost-zg'
        self.user_size       = '8'
        self.user_session    = requests.Session()

    def checkItemDirect(self):
        #NOTE: this function will most likely hamper performance but in some cases may improve it, leave it up to user choice to run this before checkout
        #Basic Steps:
        #Use BS to parse for <ul class="size options"
        #Size marked as follows: <li class="8 available" data-option-title="8"
        #Therefore, match data-option-title with user_size, then check the class for available keyword
        session_get = self.user_session.get(self.URL_direct_link)
        print 'Status of requests.get: ' + str(session_get.status_code)
        soup = BeautifulSoup(session_get.content, "lxml")
        #Check that the lxml parser works for html
        #Look to use SoupStrainer to improve parsing efficiency
        for li in soup.select('li[data-option-title]'):
            #print li['class']
            #print type(li['class'])

            if (self.user_size in li['class']) & ('available' in li['class']): 
                print 'Size ' + self.user_size + ' Available'
    
    def addToCart(self):
        session_get = self.user_session.get(self.URL_direct_link)
        print 'Status of requests.get: ' + str(session_get.status_code)
        #savePage(session_get, 'test2.html')

        soup = BeautifulSoup(session_get.content, 'lxml')
        #Check that the lxml parser works for html
        #Look to use SoupStrainer to improve parsing efficiency

        post_data = { 'id': '', 'properties[bot-key]': '' }

        #Select from inside <select id="product-select"> element
        #Find the attribute value corresponding with desired shoe size inside <option value="....">

        results = soup.find_all('select', {'id':'product-select'}) 
        foo = results[0].select('option')
        print results
        print
        print foo



        



if __name__ == '__main__':
    instance = bodegaREQ()
    instance.checkItemDirect()
    instance.addToCart()

'''
    def addToCart(self):
        #Save the line below:
        ResultSet = prod_soup.find_all('form', {'id' : 'qv-form'})
    
        ResultSetString = unicode.join(u'\n',map(unicode,ResultSet))
        ResultSoup = BeautifulSoup(ResultSetString, "lxml")
        #print ResultSoup.prettify()
        with open('bodegaForm.html', 'wb') as bodegaFormFile:
            bodegaFormFile.write(ResultSoup.prettify())

        #select: name="id" value=22348567876 (11.5)
        #input:  id="key" name="properties[bot-key]" type="hidden" value="6402243972

        post_data = { 'id':'22348567876', 'properties[bot-key]':'6402243972' }
        add_to_cart_js = 'http://shop.bdgastore.com/cart/add.js'
        session_post = user_session.post(url=add_to_cart_js, data=post_data)

        print str(session_post.status_code)

        session_get = user_session.get('http://shop.bdgastore.com/cart')
        savePage(session_get, 'bodegaCart.html')
        #Note: This shows the cart is indeed added. See <div id='cart'>
        #Possible reason this is not working: Firefox 3.x+ has a specific format for their cookies...double check this
        checkCart(user_session)

        #session_get  = user_session.get('http://shop.bdgastore.com/')
        #print str(user_session.cookies) + '\n'

        #cookies = dict_from_cookiejar(user_session.cookies)
        #print cookies

#driver = webdriver.Firefox()
#driver.add_cookie(cookies)
#driver.add_cookie({'path':'/'})
#driver.get('http://shop.bdgastore.com/cart')
#So the posted data gets accepted...but why doesn't the item show in the cart after the cookies get imported?
#Possible Reason: cart_sig cookie is empty
'''




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
