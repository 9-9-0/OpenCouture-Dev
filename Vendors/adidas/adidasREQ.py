import requests
import re
from bs4 import BeautifulSoup
import time
import json

#Vendor Specific NOTES: 
#Use chrome if you're going to emulate browser automation as the javascript lags with default Firefox

def savePage(response, filename, rate=100000):
    output = open(filename, 'wb')
    for chunk in response.iter_content(rate):
        output.write(chunk)

class adidasREQ():
    def __init__(self):
        self.URL_home_url      = 'http://www.adidas.com/us/men-shoes' #NOTE: Newest releases may not show with sort options
        self.URL_product_url   = 'http://www.adidas.com/us/superstar-triple-shoes/BB3695.html'
        self.URL_cart_url      = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show'
        self.URL_cart_post_url = 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
        self.URL_checkout_url  = 'https://www.adidas.com/us/delivery-start'
        self.URL_post_SB_url   = ''
        self.URL_pay_url       = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start'
        self.user_size         = '10'
        self.match_pattern     = re.compile("^%s+$" % self.user_size)
        self.sub_pattern       = re.compile("[\\n\\t]")
        self.user_session      = requests.Session()
        self.get_headers = {}
        self.post_headers = {}
        self.post_data_addToCart = { 'layer': 'Add To Bag overlay', 'pid': '', 'Quantity':'1', 'masterPID':'', 'ajax': 'true' }
        #NOTE: Make quantity variable at some point?
        self.post_data_custInfo = { 'dwfrm_delivery_shippingOriginalAddress': 'false',
                                    'dwfrm_delivery_shippingSuggestedAddress': 'false',
                                    'dwfrm_delivery_singleshipping_shippingAddress_isedited': 'false',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_firstName': 'Bobb',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_lastName': 'McFlymo',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address1': '1000 5th Ave',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address2': '',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_city': 'Seattle',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_countyProvince': 'WA',
                                    'state': '',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_zip': '98101',
                                    'dwfrm_delivery_singleshipping_shippingAddress_addressFields_phone': '2029001930',
                                    'dwfrm_delivery_singleshipping_shippingAddress_useAsBillingAddress': 'false',
                                    'dwfrm_delivery_securekey': '',
                                    'dwfrm_delivery_billingOriginalAddress': 'false',
                                    'dwfrm_delivery_billingSuggestedAddress': 'false',
                                    'dwfrm_delivery_billing_billingAddress_isedited': 'false',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_country': 'US',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_firstName': 'Bobb',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_lastName': 'McFlymo',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_address1': '1000 5th Ave',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_address2': '',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_city': 'Seattle',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_countyProvince': 'WA',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_zip': '98101',
                                    'dwfrm_delivery_billing_billingAddress_addressFields_phone': '2029001930',
                                    'dwfrm_delivery_singleshipping_shippingAddress_email_emailAddress': 'asfsaf@gmail.com',
                                    'signup_source': 'shipping',
                                    'dwfrm_delivery_singleshipping_shippingAddress_ageConfirmation': 'true',
                                    'shipping-group-0': 'Standard',
                                    'dwfrm_cart_shippingMethodID_0': 'Standard',
                                    'shippingMethodType_0': 'inline',
                                    'dwfrm_cart_selectShippingMethod': 'ShippingMethodID',
                                    'referer': 'Cart-Show',
                                    'dwfrm_delivery_singleshipping_shippingAddress_agreeForSubscription': 'true',
                                    'dwfrm_delivery_savedelivery': 'Review and Pay',
                                    'format': 'ajax'
                                  }
        #NOTE: Begin looking at fieldset class="shipping wrapper set" for all the necessary values
        #NOTE: IMPORTANT: self.post_data_custInfo MIGHT NOT BE the data that's sent...see Dev Notes
        #NOTE: Checked the posted form, current self.post_data_custInfo should be all that's posted

        self.importProfile()
        self.setHeaders()
    
    def importProfile(self):
        print 'ayy bae diz iz importProfile() placeholder'

    def setHeaders(self):
        self.get_headers = { 'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
                             'Accept-Encoding': 'gzip, deflate, sdch',
                             'Accept-Language': 'en-US, en;q=0.8',
                             'Connection': 'keep-alive',
                             'Host': 'www.adidas.com',
                             'Referer': self.URL_home_url,
                             'Upgrade-Insecure-Requests': '1',
                             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36'}
        #print self.get_headers
        #NOTE: */* matches all of the formats, including all the other ones so that it's less conspicuous to Adidas
        #Cookie header might not be necessary, but look into using session cookies as the value
        #self.headers['Cookie']
        #NOTE: Referer needs to be updated with each step of the process or you might be banned

        self.post_headers = { 'Accept': '*/*',
                              'Accept-Encoding': 'gzip, deflate',
                              'Accept-Language': 'en-US, en;q=0.8',
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
        print '\nADD TO CART -----------------'
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
                self.post_data_addToCart['pid'] = item['value']
                self.post_data_addToCart['masterPID'] = item['value'].partition("_")[0]
                print self.post_data_addToCart
                break

        session_post = self.user_session.post(url=self.URL_cart_post_url, headers=self.post_headers, data=self.post_data_addToCart)
        print 'Add To Cart Status: ' + str(session_post.status_code)

    def inspectCart(self):
        #NOTE: Optional step, however suspicion may be raised from examining the referer value (when manually adding to cart,
        #      if the checkout is prompted from the product page, a format with a variable value is set as the referer value)
        #      For now, this should be run to show that the cart was visited prior to checkout
        print '\nINSPECT CART ----------------'
        self.get_headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
        self.get_headers['Referer'] = self.URL_product_url
        #print self.get_headers
        session_get = self.user_session.get(url=self.URL_cart_url, headers=self.get_headers)

        print 'Inspect Cart Status: ' + str(session_get.status_code)
        
        #savePage(session_get, 'cartContents.html')

    def enterShipBill(self):
        print '\nEntering Shipping + Billing Info -------------------'
        
        #Modify Headers
        self.get_headers['Referer'] = self.URL_cart_url
        self.post_headers['Accept'] = 'text/html, */*; q=0.01'
        self.post_headers['Accept-Encoding'] = 'gzip, deflate, br'
        #self.post_headers['Content-Length'] = '2500' #May get rid of this, seems to respond to length of data posted possibly sets a limit
        self.post_headers.pop('Content-Length')
        self.post_headers['Referer'] = self.URL_checkout_url
        #NOTE: self.URL_pay_url is the correct referer value if done from a clean session
        #result = soup.find('meta', {'property': 'og:url'})
        #Future reference: the basket key is stored in cookies
        #print 'enterShipBill GET HEADERS'
        #print json.dumps(self.get_headers, indent=1)

        session_get = self.user_session.get(self.URL_checkout_url, headers=self.get_headers)
        #savePage(session_get, 'ShipBillPage.html')

        soup = BeautifulSoup(session_get.content, 'lxml')
        result = soup.find('input', {'name':'dwfrm_delivery_securekey'})
        self.post_data_custInfo['dwfrm_delivery_securekey'] = result['value']
        result = soup.find('form', class_='formcheckout') 
        self.URL_post_SB_url = result['action']
        #print self.URL_post_SB_url
        #print 'enterShipBill POST HEADERS'
        #print json.dumps(self.post_headers, indent=1)
        #print 'enterShipBill POST DATA'
        #print json.dumps(self.post_data_custInfo, indent=1)

        session_post = self.user_session.post(url=self.URL_post_SB_url, headers=self.post_headers, data=self.post_data_custInfo)

        print 'enterShipBill Status: ' + str(session_post.status_code)

    def finalBoss(self):
        print '\nEntering Payment Info -----------------------------'
        self.get_headers['Referer'] = self.URL_checkout_url
        #print json.dumps(self.get_headers, indent=1)
        session_get = self.user_session.get(self.URL_pay_url, headers=self.get_headers)
        

        savePage(session_get, 'finalCheckout.html')


if __name__=='__main__':
    start_time = time.time()
    instance = adidasREQ()
    instance.addToCart()
    instance.inspectCart()
    instance.enterShipBill()
    instance.finalBoss()
    print("%s seconds" % (time.time() - start_time))

