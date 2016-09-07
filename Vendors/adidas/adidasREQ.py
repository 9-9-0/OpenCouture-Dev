import requests
from bs4 import BeautifulSoup

#Vendor Specific NOTES: 
#Use chrome if you're going to emulate browser automation as the javascript lags with default Firefox

class adidasREQ():
    def __init__(self):
        self.URL_vendor_url  = 'http://www.adidas.com/us/men-originals-shoes' #Note: Newest releases may not show with sort options
        self.URL_direct_link = 'http://www.adidas.com/us/superstar-triple-shoes/BB3695.html'
        self.user_size       = '8'
        self.user_session    = requests.Session()
        self.headers = {}
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
        print self.headers
    def addToCart(self):
        self.setHeaders()
        session_get = self.user_session.get(self.URL_direct_link, headers=self.headers)
        print session_get.content
        #Server rejects request. Possibly modify a header

if __name__=='__main__':
    instance = adidasREQ()
    instance.addToCart()

