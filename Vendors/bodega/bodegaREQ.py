import requests
from requests.utils import dict_from_cookiejar
from bs4 import BeautifulSoup
from selenium import webdriver
import code
import webbrowser
import re
import time
#NOTES: 
# Header functionalities not implemented for this process, might add it in later

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

class bodegaREQ():
    def __init__(self):
        self.URL_vendor      = 'http://shop.bdgastore.com/'
        self.URL_product     = 'http://shop.bdgastore.com/collections/footwear/products/y-3-pureboost-zg'
        self.URL_addToCart   = 'http://shop.bdgastore.com/cart/add.js'
        self.URL_cart        = 'http://shop.bdgastore.com/cart'
        self.user_size       = '8'
        self.user_session    = requests.Session()

    def checkItemDirect(self):
        #NOTE: this function will most likely hamper performance but in some cases may improve it, leave it up to user choice to run this before checkout
        #Basic Steps:
        #Use BS to parse for <ul class="size options"
        #Size marked as follows: <li class="8 available" data-option-title="8"
        #Therefore, match data-option-title with user_size, then check the class for available keyword
        session_get = self.user_session.get(self.URL_product)
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
        session_get = self.user_session.get(self.URL_product)
        print 'Status of requests.get: ' + str(session_get.status_code)
        #savePage(session_get, 'test2.html')

        soup = BeautifulSoup(session_get.content, 'lxml')
        #Check that the lxml parser works for html
        #Look to use SoupStrainer to improve parsing efficiency

        post_data = { 'id': '', 'properties[bot-key]': '' }
        
        #Find bot key
        results = soup.find('input', {'name':'properties[bot-key]'})
        post_data['properties[bot-key]'] = results['value']

        #Find corresponding size value
        results = soup.find_all('select', {'id':'product-select'}) 
        for option in results[0].select('option'):
            size = re.sub('.* \/.', '', str(option.contents))
            size = re.sub('.-.*', '', size)
            if (size == self.user_size):
                post_data['id'] = option['value']
                #print post_data

        session_post = self.user_session.post(url=self.URL_addToCart, data=post_data)

        print "Add to cart post status: " + str(session_post.status_code)
        #savePage(session_get, 'bodegaCart.html')

    def loadCartAndCheckout(self):
        #Import Cookies
        driver = webdriver.Chrome(executable_path="./chromedriver")
        driver.delete_all_cookies()
        driver.get(self.URL_cart)

        cookies = requests.utils.dict_from_cookiejar(self.user_session.cookies)
        
        for cookie in cookies.items():
            cookie_dict = {'name': '',
                           'value': '',
                           'path': '/'}
            cookie_dict['name'] = cookie[0]
            cookie_dict['value'] = cookie[1]
            driver.add_cookie(cookie_dict)
                          
        driver.get(self.URL_cart)
        #time.sleep(5)
        #driver.quit()


if __name__ == '__main__':
    instance = bodegaREQ()
    instance.checkItemDirect()
    instance.addToCart()
    instance.loadCartAndCheckout()
