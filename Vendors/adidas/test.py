import requests
import re
from bs4 import BeautifulSoup

#Vendor Specific NOTES: 
#Use chrome if you're going to emulate browser automation as the javascript lags with default Firefox

class adidasREQ():
    def __init__(self):
        self.URL_vendor_url  = 'http://www.adidas.com/us/men-originals-shoes' #Note: Newest releases may not show with sort options
        self.URL_direct_link = 'http://www.adidas.com/us/superstar-triple-shoes/BB3695.html'
        self.user_size       = '10'
        self.match_pattern   = re.compile("^%s+$" % self.user_size)
        self.sub_pattern     = re.compile("[\\n\\t]")
        self.user_session    = requests.Session()
        self.headers = {}

        self.setHeaders()
    def setHeaders(self):
        self.headers['Accept'] = ['text/html', 'application/xhtml+xml', 'application/xml;q=0.9', 'image/webp', '*/*;q=0.8']
        self.headers['Accept-Encoding'] = ['gzip', 'deflate', 'sdch']
        self.headers['Accept-Language'] = ['en-US', 'en;q=0.8']
        self.headers['Cache-Control'] = 'max-age=0'
        self.headers['Connection'] = 'keep-alive'
        #Cookie header might not be necessary
        #self.headers['Cookie']
        self.headers['Host'] = 'www.adidas.com'
        self.headers['Upgrade-Insecure-Requests'] = '1'
        self.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36'
        #print self.headers
    def addToCart(self):
        self.setHeaders() # This needs to be done prior to task execution
        post_data = { 'layer': 'Add To Bag overlay', 'pid': '', 'Quantity':'1', 'masterPID':'', 'ajax': 'true' }
        #Note: Some fields may not be needed, make quantity variable at some point?          
        post_url  = 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
                      
        session_get = self.user_session.get(self.URL_direct_link, headers=self.headers)
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

        session_post = self.user_session.post(url=post_url, headers=self.headers, data=post_data)

        print session_post.status_code

        session_get = self.user_session.get(url='https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show', headers=self.headers)

        print session_get.status_code
        
        output = open('cartContents.html', 'wb')
        for chunk in session_get.iter_content(1000000):
            output.write(chunk)


if __name__=='__main__':
    instance = adidasREQ()
    instance.addToCart()

