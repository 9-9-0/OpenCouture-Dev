import mechanize
import cookielib
from selenium import webdriver
from requests.utils import dict_from_cookiejar
import re

class bodegaMECH():
    def __init__(self):
        self.br = mechanize.Browser()
        #self.cj = cookielib.LWPCookieJar()
        self.cj = cookielib.MozillaCookieJar()

        self.br.set_cookiejar(self.cj)
        self.br.set_handle_equiv(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Firefox')]

        self.item_url = 'http://shop.bdgastore.com/collections/footwear/products/y-3-pureboost-zg'

        # Create variables for user credentials and a function to import them
    def addToCart(self):
        self.br.open(self.item_url)
        #If possible, remove formcount search from runtime
        formcount=0
        for form in self.br.forms():
            if str(form.attrs.get('id'))=='qv-form':
                break
            formcount=formcount+1

        self.br.select_form(nr=formcount)
        self.br['id'] = ['22348567876']
        #br['properties[bot-key]'] = '6402243972'
        resp = self.br.submit()
        #print resp

        resp = self.br.open('http://shop.bdgastore.com/cart')
        #print resp.read()
        #Check the div id=cart, this successfully adds item to cart

    def checkCart(self):
        print self.cj
        
        #driver = webdriver.Firefox()
        #driver.add_cookie(cj_dict)
        #driver.get('http://shop.bdgastore.com/cart')
        #print(driver.get_cookies())
        #for cookie in self.cj:
        #    print cookie.name, cookie.value, cookie.domain
        #try importing cookies manually vs using the requests util

        #driver = webdriver.Chrome('./chromedriver')
        
if __name__=='__main__':
    instance = bodegaMECH()
    instance.addToCart()
    instance.checkCart()
