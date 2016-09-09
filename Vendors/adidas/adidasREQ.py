import requests
import re
from bs4 import BeautifulSoup

#Vendor Specific NOTES: 
#Use chrome if you're going to emulate browser automation as the javascript lags with default Firefox

class adidasREQ():
    def __init__(self):
        self.URL_vendor_url    = 'http://www.adidas.com/us/men-originals-shoes' #NOTE: Newest releases may not show with sort options
        self.URL_product_url   = 'http://www.adidas.com/us/superstar-triple-shoes/BB3695.html'
        self.URL_cart_url      = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show'
        self.URL_cart_post_url = 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
        self.URL_checkout_url  = 'https://www.adidas.com/us/delivery-start'
        self.user_size         = '10'
        self.match_pattern     = re.compile("^%s+$" % self.user_size)
        self.sub_pattern       = re.compile("[\\n\\t]")
        self.user_session      = requests.Session()
        self.get_headers = {}
        self.post_headers = {}

        self.importProfile()
        self.setHeaders()
    
    def importProfile(self):
        print 'ayy bae diz iz importProfile() placeholder'

    def setHeaders(self):
        self.get_headers = { 'Accept': ['text/html', 'application/xhtml+xml', 'application/xml;q=0.9', 'image/webp', '*/*;q=0.8'],
                             'Accept-Encoding': ['gzip', 'deflate', 'sdch'],
                             'Accept-Language': ['en-US', 'en;q=0.8'],
                             'Cache-Control': 'max-age=0',
                             'Connection': 'keep-alive',
                             'Host': 'www.adidas.com',
                             'Referer': self.URL_vendor_url,
                             'Upgrade-Insecure-Requests': '1',
                             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36'}
        #print self.get_headers
        #NOTE: */* matches all of the formats, including all the other ones so that it's less conspicuous to Adidas
        #Cookie header might not be necessary, but look into using session cookies as the value
        #self.headers['Cookie']
        #NOTE: Referer needs to be updated with each step of the process or you might be banned

        self.post_headers = { 'Accept': '*/*',
                              'Accept-Encoding': ['gzip', 'deflate'],
                              'Accept-Language': ['en-US', 'en;q=0.8'],
                              'Connection': 'keep-alive',
                              'Content-Length': '77',
                              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                              'Host': 'www.adidas.com',
                              'Origin': 'www.adidas.com',
                              'Referer': self.URL_product_url,
                              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36',
                              'X-Requested-With': 'XMLHttpRequest' }
        #print self.post_headers

    def addToCart(self):
        post_data = { 'layer': 'Add To Bag overlay', 'pid': '', 'Quantity':'1', 'masterPID':'', 'ajax': 'true' }
        #NOTE: Make quantity variable at some point?          
                      
        session_get = self.user_session.get(self.URL_product_url, headers=self.get_headers)
        #print session_get.content
        soup = BeautifulSoup(session_get.content, 'lxml')
        
        results = soup.find_all('select', class_='size-select')
        #print results

        for item in results[0].select('option'):
            re_result = re.sub(self.sub_pattern, '', item.string)
            #print re_result
            matchObj = re.search(r"^%s+$" % self.user_size, re_result)
            if matchObj:
                post_data['pid'] = item['value']
                post_data['masterPID'] = item['value'].partition("_")[0]
                #print post_data

        session_post = self.user_session.post(url=self.URL_cart_url, headers=self.post_headers, data=post_data)
        print 'Add To Cart Status: ' + str(session_post.status_code)

    def inspectCart(self):
        print
        self.get_headers['Referer'] = self.URL_product_url
        print self.get_headers
        session_get = self.user_session.get(url=self.URL_cart_url, headers=self.get_headers)

        print 'Inspect Cart Status: ' + session_get.status_code
        
        #output = open('cartContents.html', 'wb')
        #for chunk in session_get.iter_content(1000000):
        #    output.write(chunk)

    def checkOut(self):
        #self.headers['Referer'] = 
        session_get = self.user_session.get(self.URL_checkout_url, headers=self.headers)

        soup = BeautifulSoup(session_get.contents, 'lxml')

        #output = open('checkout1.html', 'wb')
        #for chunk in session_get.iter_content(100000):
        #    output.write(chunk)



if __name__=='__main__':
    instance = adidasREQ()
    instance.addToCart()
    instance.inspectCart()
    #instance.checkOut()

